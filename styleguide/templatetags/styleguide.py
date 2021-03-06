import os.path
from html.parser import HTMLParser
from textwrap import dedent
from inspect import getsourcefile

from django import template
from django.utils.safestring import SafeString
from django.utils.module_loading import import_string
from django.utils.html import escape
from django.utils.text import slugify


BASE_GITHUB_URL = 'https://github.com/18F/calc'

DEFAULT_GITHUB_BRANCH = 'develop'

MY_DIR = os.path.abspath(os.path.dirname(__file__))

ROOT_DIR = os.path.normpath(os.path.join(MY_DIR, '..', '..'))

register = template.Library()


@register.tag
def guide(parser, token):
    '''
    A {% guide %} represents an HTML document composed into sections with a
    table of contents linking to them.
    '''

    nodelist = parser.parse(('endguide',))
    parser.delete_first_token()
    return GuideNode(nodelist)


class GuideNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        context['_sections'] = []

        html = self.nodelist.render(context)

        t = context.template.engine.get_template('styleguide_with_toc.html')

        result = t.render(template.Context({
            'html': html,
            'sections': context['_sections']
        }))

        del context['_sections']

        return result


def github_url_for_path(path):
    '''
    Given a relative path from the root of the repository, returns a
    GitHub URL to its syntax-highlighted source code.
    '''

    return '{}/tree/{}/{}'.format(
        BASE_GITHUB_URL,
        DEFAULT_GITHUB_BRANCH,
        path
    )


class WebComponentHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.tag = tag
        self.extends = ''
        for attr, val in attrs:
            if attr == 'is':
                self.extends = val


@register.simple_tag
def webcomponent(html):
    '''
    Link to the source code of a web component, e.g. <foo> or
    <input is="bar">.

    This actually renders markup that client-side code will resolve into
    a definitive link via introspecting the JS runtime environment. The
    front-end will raise an error if the web component or its source code
    can't be found, to help prevent documentation rot.
    '''

    parser = WebComponentHTMLParser()
    parser.feed(html)
    return SafeString(
        '<code><a is="web-component-link" href="{}" '
        'data-tag="{}" data-extends="{}">{}</a></code>'.format(
            escape(github_url_for_path('')),
            escape(parser.tag),
            escape(parser.extends),
            escape(html)
        )
    )


@register.simple_tag
def pyobjname(name):
    '''
    Outputs a link to the source code of the given Python object (e.g.
    module, function, class, etc).

    If the object can't be found, raises an exception. This is primarily
    done to prevent documentation rot.
    '''

    obj = import_string(name)
    filename = os.path.relpath(getsourcefile(obj), ROOT_DIR)

    return SafeString('<code><a href="{}">{}</a></code>'.format(
        escape(github_url_for_path(filename)),
        escape(name)
    ))


@register.simple_tag
def pathname(name):
    '''
    Outputs a link to the source code of the given project-relative path.

    If the path doesn't exist, raises an exception. This is primarily
    done to prevent documentation rot.
    '''

    if not os.path.exists(os.path.join(ROOT_DIR, name)):
        raise Exception('Path %s does not exist' % name)

    return SafeString('<code><a href="{}">{}</a></code>'.format(
        escape(github_url_for_path(name)),
        escape(name)
    ))


@register.simple_tag(takes_context=True)
def guide_section(context, name):
    '''
    A section in a guide. It must be used within a {% guide %} tag.
    '''

    if '_sections' not in context:
        raise Exception(r'{% guide_section %} tags should only be used '
                        r'within {% guide%} tags!')
    section = Section(name)
    context['_sections'].append(section)
    t = context.template.engine.get_template('styleguide_section.html')

    return t.render(template.Context({'section': section}))


class Section:

    def __init__(self, name):
        self.name = name
        self.id = slugify(name)


@register.tag
def example(parser, token):
    '''
    An HTML code snippet example in a style guide. Includes both the
    rendered version of the example and the source code.
    '''

    nodelist = parser.parse(('endexample',))
    parser.delete_first_token()
    return ExampleNode(nodelist)


class ExampleNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        html = SafeString(dedent(self.nodelist.render(context)).strip())

        t = context.template.engine.get_template('styleguide_example.html')

        return t.render(template.Context({'html': html}))
