import datetime
from decimal import Decimal
from itertools import cycle

from django.test import TestCase
from contracts.mommy_recipes import get_contract_recipe

from ..models import Contract, convert_to_tsquery


class ContractTestCase(TestCase):
    def make_contract_with_rates(self, **kwargs):
        final_kwargs = dict(
            hourly_rate_year1=100.00,
            hourly_rate_year2=102.20,
            hourly_rate_year3=103.30,
            hourly_rate_year4=104.40,
            hourly_rate_year5=105.50)
        final_kwargs.update(kwargs)
        return get_contract_recipe().make(**final_kwargs)

    def test_readable_business_size(self):
        business_sizes = ('O', 'S')
        contract1, contract2 = get_contract_recipe().make(
            _quantity=2, business_size=cycle(business_sizes))
        self.assertEqual(contract1.get_readable_business_size(),
                         'other than small business')
        self.assertEqual(
            contract2.get_readable_business_size(), 'small business')

    def test_get_education_code(self):
        c = get_contract_recipe().make()
        self.assertEqual(c.get_education_code('Bachelors'), 'BA')
        self.assertIsNone(c.get_education_code('Nursing'), None)

    def test_normalize_rate(self):
        c = get_contract_recipe().make()
        self.assertEqual(c.normalize_rate('$1,000.00,'), 1000.0)

    def test_convert_to_tsquery(self):
        self.assertEqual(convert_to_tsquery(
            'staff  consultant'), 'staff:* & consultant:*')
        self.assertEqual(convert_to_tsquery(
            'senior typist (st)'), 'senior:* & typist:* & st:*')
        self.assertEqual(convert_to_tsquery('@$(#)%&**#'), '')

    def test_get_hourly_rate(self):
        c = self.make_contract_with_rates()
        self.assertEqual(c.get_hourly_rate(1), 100.00)
        self.assertEqual(c.get_hourly_rate(2), 102.20)
        self.assertEqual(c.get_hourly_rate(3), 103.30)
        self.assertEqual(c.get_hourly_rate(4), 104.40)
        self.assertEqual(c.get_hourly_rate(5), 105.50)

    def test_get_hourly_rate_raises_on_invalid_year(self):
        c = get_contract_recipe().make()
        with self.assertRaises(ValueError):
            c.get_hourly_rate(0)
        with self.assertRaises(ValueError):
            c.get_hourly_rate(6)

    def test_set_hourly_rate(self):
        c = get_contract_recipe().make()
        for i in range(1, 6):
            c.set_hourly_rate(i, 120)
            self.assertEqual(
                getattr(c, 'hourly_rate_year{}'.format(i)), 120)

    def test_set_hourly_rate_raises_on_invalid_year(self):
        c = get_contract_recipe().make()
        with self.assertRaises(ValueError):
            c.set_hourly_rate(0, 50)
        with self.assertRaises(ValueError):
            c.set_hourly_rate(6, 50)

    def test_escalate_hourly_rate_fields(self):
        c = get_contract_recipe().make()
        c.escalate_hourly_rate_fields(base_year_rate=100,
                                      escalation_rate=2.5)
        self.assertEqual(c.hourly_rate_year1, 100)
        self.assertAlmostEqual(c.hourly_rate_year2, Decimal(102.50), places=2)
        self.assertAlmostEqual(c.hourly_rate_year3, Decimal(105.06), places=2)
        self.assertAlmostEqual(c.hourly_rate_year4, Decimal(107.69), places=2)
        self.assertAlmostEqual(c.hourly_rate_year5, Decimal(110.38), places=2)

    def test_escalate_sets_prices_to_base_year_rate_when_no_escalation(self):
        c = get_contract_recipe().make()
        c.escalate_hourly_rate_fields(base_year_rate=125.40,
                                      escalation_rate=0)
        self.assertEqual(c.hourly_rate_year1, 125.40)
        self.assertEqual(c.hourly_rate_year2, 125.40)
        self.assertEqual(c.hourly_rate_year3, 125.40)
        self.assertEqual(c.hourly_rate_year4, 125.40)
        self.assertEqual(c.hourly_rate_year5, 125.40)

    def test_escalate_hourly_rate_fields_raises_on_invalid_rate(self):
        c = get_contract_recipe().make()
        with self.assertRaises(ValueError):
            c.escalate_hourly_rate_fields(base_year_rate=100,
                                          escalation_rate=-5)
        with self.assertRaises(ValueError):
            c.escalate_hourly_rate_fields(base_year_rate=100,
                                          escalation_rate=100)
        with self.assertRaises(ValueError):
            c.escalate_hourly_rate_fields(base_year_rate=100,
                                          escalation_rate=99.1)

    def test_update_price_fields(self):
        c = self.make_contract_with_rates(
            contract_start=datetime.date(2016, 2, 11),
            contract_end=datetime.date(2021, 2, 11))

        c.contract_year = 1
        c.update_price_fields()
        self.assertEqual(c.current_price, 100.00)
        self.assertEqual(c.next_year_price, 102.20)
        self.assertEqual(c.second_year_price, 103.30)

        c.contract_year = 2
        c.update_price_fields()
        self.assertEqual(c.current_price, 102.20)
        self.assertEqual(c.next_year_price, 103.30)
        self.assertEqual(c.second_year_price, 104.40)

        c.contract_year = 3
        c.update_price_fields()
        self.assertEqual(c.current_price, 103.30)
        self.assertEqual(c.next_year_price, 104.40)
        self.assertEqual(c.second_year_price, 105.50)

        c.contract_year = 4
        c.update_price_fields()
        self.assertEqual(c.current_price, 104.40)
        self.assertEqual(c.next_year_price, 105.50)
        self.assertIsNone(c.second_year_price)

        c.contract_year = 5
        c.update_price_fields()
        self.assertEqual(c.current_price, 105.50)
        self.assertIsNone(c.next_year_price)
        self.assertIsNone(c.second_year_price)

    def test_update_price_fields_works_for_future_contract_start(self):
        c = self.make_contract_with_rates(
            contract_start=datetime.date(2016, 2, 11),
            contract_end=datetime.date(2020, 2, 11))

        c.contract_year = 1
        c.update_price_fields()
        self.assertEqual(c.current_price, 100.00)
        self.assertEqual(c.next_year_price, 102.20)
        self.assertEqual(c.second_year_price, 103.30)

        c.contract_year = 0
        c.update_price_fields()
        self.assertEqual(c.current_price, None)
        self.assertEqual(c.next_year_price, 100.00)
        self.assertEqual(c.second_year_price, 102.20)

        c.contract_year = -1
        c.update_price_fields()
        self.assertEqual(c.current_price, None)
        self.assertEqual(c.next_year_price, None)
        self.assertEqual(c.second_year_price, 100.00)

        c.contract_year = -2
        c.update_price_fields()
        self.assertEqual(c.current_price, None)
        self.assertEqual(c.next_year_price, None)
        self.assertEqual(c.second_year_price, None)

    def test_update_price_fields_sets_to_None_when_current_year_gt_5(self):
        c = get_contract_recipe().make(
            contract_year=6,
            contract_start=datetime.date(2017, 2, 11),
            contract_end=datetime.date(2021, 2, 11))
        c.update_price_fields()
        self.assertIsNone(c.current_price)
        self.assertIsNone(c.next_year_price)
        self.assertIsNone(c.second_year_price)

    def test_update_price_fields_raises_when_no_contract_year(self):
        c = get_contract_recipe().make(contract_year=None)
        with self.assertRaises(ValueError):
            c.update_price_fields()

    def test_update_price_fields_takes_contract_end_into_account(self):
        c = self.make_contract_with_rates(
            contract_year=1,
            contract_start=datetime.date(2016, 2, 11),
            contract_end=datetime.date(2017, 1, 1))

        c.update_price_fields()
        self.assertEqual(c.current_price, 100.00)
        self.assertEqual(c.next_year_price, None)
        self.assertEqual(c.second_year_price, None)

        c.contract_end = datetime.date(2018, 1, 1)
        c.update_price_fields()
        self.assertEqual(c.current_price, 100.00)
        self.assertEqual(c.next_year_price, 102.20)
        self.assertEqual(c.second_year_price, None)

        c.contract_end = datetime.date(2019, 1, 1)
        c.update_price_fields()
        self.assertEqual(c.current_price, 100.00)
        self.assertEqual(c.next_year_price, 102.20)
        self.assertEqual(c.second_year_price, 103.30)

    def test_adjust_contract_year(self):
        c = get_contract_recipe().make(
            contract_start=datetime.date(2016, 2, 11))
        c.adjust_contract_year(
            current_date=datetime.date(2016, 2, 12))
        self.assertEqual(c.contract_year, 1)

        c.adjust_contract_year(
            current_date=datetime.date(2015, 2, 1))
        self.assertEqual(c.contract_year, 0)

    def test_adjust_contract_year_raises_when_no_contract_start(self):
        c = get_contract_recipe().make(contract_start=None)
        with self.assertRaises(ValueError):
            c.adjust_contract_year()

    def test_calculate_end_year(self):
        c = get_contract_recipe().make(
            contract_start=datetime.date(2016, 2, 11),
            contract_end=datetime.date(2020, 2, 12))
        self.assertEqual(c.calculate_end_year(), 5)

        c.contract_end = datetime.date(2018, 2, 12)
        self.assertEqual(c.calculate_end_year(), 3)

    def test_calculate_end_year_maxes_at_5(self):
        c = get_contract_recipe().make(
            contract_start=datetime.date(2016, 2, 11),
            contract_end=datetime.date(2030, 2, 12))
        self.assertEqual(c.calculate_end_year(), 5)

    def test_calculate_end_year_raises_when_no_contract_start_or_end(self):
        d = datetime.date(2016, 2, 11)
        c = get_contract_recipe().make(
            contract_start=None,
            contract_end=d)
        with self.assertRaises(ValueError):
            c.calculate_end_year()
        c.contract_start = d
        c.contract_end = None
        with self.assertRaises(ValueError):
            c.calculate_end_year()

    def test_calculate_end_year_raises_when_start_after_end(self):
        c = get_contract_recipe().make(
            contract_start=datetime.date(2020, 2, 11),
            contract_end=datetime.date(2015, 2, 12))
        with self.assertRaises(ValueError):
            c.calculate_end_year()


class ContractSearchTestCase(TestCase):
    CATEGORIES = [
        'Sign Language Interpreter',
        'Foreign Language Staff Interpreter (Spanish sign language)',
        'Aircraft Servicer',
        'Service Order Dispatcher',
        'Disposal Services',
        'Interpretation Services Class 4: Afrikan,Akan,Albanian',
        'Interpretation Services Class 1: Spanish',
        'Interpretation Services Class 2: French, German, Italian',
    ]

    def assertCategoriesEqual(self, results, categories):
        result_categories = [r.labor_category for r in results]
        self.assertEqual(sorted(result_categories), sorted(categories))

    def setUp(self):
        self.contracts = get_contract_recipe().make(
            labor_category=cycle(self.CATEGORIES),
            _quantity=len(self.CATEGORIES)
        )

    def test_multi_phrase_search_works_with_single_word_phrase(self):
        results = Contract.objects.multi_phrase_search('interpretation')
        self.assertCategoriesEqual(results, [
            u'Sign Language Interpreter',
            u'Foreign Language Staff Interpreter (Spanish sign language)',
            u'Interpretation Services Class 4: Afrikan,Akan,Albanian',
            u'Interpretation Services Class 1: Spanish',
            u'Interpretation Services Class 2: French, German, Italian'
        ])

    def test_multi_phrase_search_works_with_multi_word_phrase(self):
        results = Contract.objects.multi_phrase_search([
            'interpretation services'
        ])
        self.assertCategoriesEqual(results, [
            u'Interpretation Services Class 4: Afrikan,Akan,Albanian',
            u'Interpretation Services Class 1: Spanish',
            u'Interpretation Services Class 2: French, German, Italian'
        ])

    def test_multi_phrase_search_works_with_multiple_phrases(self):
        results = Contract.objects.multi_phrase_search([
            'interpretation services',
            'disposal'
        ])
        self.assertCategoriesEqual(results, [
            u'Disposal Services',
            u'Interpretation Services Class 4: Afrikan,Akan,Albanian',
            u'Interpretation Services Class 1: Spanish',
            u'Interpretation Services Class 2: French, German, Italian'
        ])

    def test_search_index_works_via_raw_sql(self):
        results = Contract.objects.raw(
            '''
            SELECT id, labor_category
            FROM contracts_contract
            WHERE search_index @@ to_tsquery('Interpretation')
            ORDER BY id
            '''
        )
        self.assertCategoriesEqual(results, [
            u'Sign Language Interpreter',
            u'Foreign Language Staff Interpreter (Spanish sign language)',
            u'Interpretation Services Class 4: Afrikan,Akan,Albanian',
            u'Interpretation Services Class 1: Spanish',
            u'Interpretation Services Class 2: French, German, Italian'
        ])
