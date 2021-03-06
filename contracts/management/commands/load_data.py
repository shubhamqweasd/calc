import os
import logging

from django.core.management import BaseCommand
from optparse import make_option
from django.core.management import call_command

from contracts.models import Contract, BulkUploadContractSource
from contracts.loaders.region_10 import Region10Loader


class Command(BaseCommand):

    default_filename = 'contracts/docs/hourly_prices.csv'

    option_list = BaseCommand.option_list + (
        make_option(
            '-f', '--filename',
            default=default_filename,
            help='input filename (.csv, default {})'.format(default_filename)
        ),
    )

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)

        log.info("Begin load_data task")

        log.info("Deleting existing contract records")
        Contract.objects.all().delete()

        filename = options['filename']
        if not filename or not os.path.exists(filename):
            raise ValueError('invalid filename')

        log.info("Processing new datafile")

        # create BulkUploadContractSource to associate with the new Contracts
        f = open(filename, 'rb')
        upload_source = BulkUploadContractSource.objects.create(
            has_been_loaded=True,
            original_file=f.read(),
            file_mime_type="text/csv",
            procurement_center=BulkUploadContractSource.REGION_10
        )
        f.close()

        contracts = Region10Loader().load_file(
            filename, upload_source=upload_source
        )

        log.info("Inserting records")
        Contract.objects.bulk_create(contracts)

        log.info("Updating search index")
        call_command('update_search_field',
                     Contract._meta.app_label, Contract._meta.model_name)

        log.info("End load_data task")
