# encoding: utf-8

'''📜 Dicominator theme: template tags.'''


from ..models import Footer
from django import template
from django.template.context import Context
from django.urls import reverse
from wagtail.models import Site  #, Page
from wagtailmenus.models import FlatMenu
from wagtailmenus.templatetags.menu_tags import flat_menu


register = template.Library()


@register.inclusion_tag('jpl.labcas.dicominator.theme/menus/footer-menus.html', takes_context=True)
def jpl_footer_menus(context: Context) -> dict:
    menus = FlatMenu.objects.filter(handle__startswith='footer-').order_by('title')
    return {'menus': menus, 'original_context': context}


@register.simple_tag(takes_context=True)
def request_restoring_flat_menu(context: Context, original_context: Context, **kwargs):
    context['request'] = original_context['request']
    rc = flat_menu(context, **kwargs)
    return rc


@register.inclusion_tag('jpl.labcas.dicominator.theme/colophon-byline.html', takes_context=False)
def jpl_colophon_byline() -> dict:
    byline, footer = {}, Footer.for_site(Site.objects.filter(is_default_site=True).first())
    byline['manager'] = footer.site_manager if footer.site_manager else 'unknown'
    byline['webmaster'] = footer.webmaster if footer.webmaster else 'unknown'
    byline['clearance'] = footer.clearance if footer.clearance else 'unknown'
    return byline


@register.inclusion_tag('jpl.labcas.dicominator.theme/login-link.html', takes_context=True)
def login_link(context: Context) -> dict:
    request, params = context.get('request'), {}
    if request.user.is_authenticated:
        params['authenticated'] = True
        try:
            params['name'] = request.user.ldap_user.attrs['cn'][0]
        except (AttributeError, KeyError, IndexError, TypeError):
            params['name'] = f'{request.user.first_name} {request.user.last_name}'.strip()
        params['logout'] = reverse('wagtailadmin_logout') + '?next=' + request.path
    else:
        params['authenticated'], params['login'] = False, reverse('wagtailadmin_home')
    return params
