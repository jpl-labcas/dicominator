# encoding: utf-8

'''📜 Dicominator: site bloomer.'''


from jpl.labcas.dicominator.theme.models import Footer
from django.conf import settings
from django.core.management.base import BaseCommand
from jpl.labcas.dicominator.content.models import HomePage
from jpl.labcas.dicominator.tags.models import PatientIndex, TagIndex
from wagtail.models import Site, Page
from wagtail.rich_text import RichText
from wagtailmenus.models import FlatMenu, FlatMenuItem
import argparse


class Command(BaseCommand):
    help = 'Blooms the Dicominator with initial content'
    _hostname = 'labcas-dev.jpl.nasa.gov'
    _port = 80
    _description = 'EDRN DICOM census and other metrics'
    _seo_title = 'DICOM imaging format use by LabCAS and its census and other metrics'
    _ldap_uri = 'ldaps://edrn-ds.jpl.nasa.gov'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--hostname', help='Hostname of the site (default: %(default)s)', default=self._hostname)
        parser.add_argument('--port', help='Port of the site (default %(default)s)', default=self._port, type=int)
        parser.add_argument('--ldap-uri', help='URI of EDRN LDAP (default: %(default)s)', default=self._ldap_uri)

    def set_site(self, hostname: str, port: int):
        '''Set up the Wagtail `Site` object for the Dicominator.'''

        self.stdout.write('Setting up Wagtail "Site" object')
        site = Site.objects.filter(is_default_site=True).first()
        site.site_name, site.hostname, site.port = 'Dicominator', hostname, port
        site.save()
        old_root = site.root_page.specific
        if old_root.title == 'Dicominator':
            home_page = old_root
        else:
            mega_root = old_root.get_parent()

            self.stdout.write('Creating home page')
            home_page = HomePage(
                title='Dicominator', draft_title='📜 Dicominator', seo_title=self._seo_title,
                search_description=self._description.strip(), live=True, slug=old_root.slug, path=old_root.path,
                depth=old_root.depth, url_path=old_root.url_path,
            )
            home_page.body.append(('rich_text', RichText('<h1>The Dicominator</h1>')))
            home_page.body.append(('rich_text', RichText("<p>A census, analyzer, catalog, anomaly detector, and utility for DICOM tags in the Early Detection Research Network.</p>")))
            site.root_page = home_page
            old_root.delete()
            mega_root.save()
            home_page.save()
            site.save()

        # Create PatientIndex page if it doesn't exist
        if not PatientIndex.objects.child_of(home_page).exists():
            self.stdout.write('Creating PatientIndex page')
            patient_index = PatientIndex(
                title='Patients',
                draft_title='📋 Patients',
                slug='patients',
                live=True,
            )
            home_page.add_child(instance=patient_index)
            patient_index.save()
            
            # Add a link to the PatientIndex in the home page's body
            home_page.body.append(('rich_text', RichText(
                f'<p><a href="{patient_index.url}">Browse DICOM Patients</a></p>'
            )))
            home_page.save()

        # Create TagIndex page if it doesn't exist
        if not TagIndex.objects.child_of(home_page).exists():
            self.stdout.write('Creating TagIndex page')
            tag_index = TagIndex(
                title='Tags',
                draft_title='📋 Tags',
                slug='tags',
                live=True,
            )
            home_page.add_child(instance=tag_index)
            tag_index.save()
            
            # Add a link to the TagIndex in the home page's body
            home_page.body.append(('rich_text', RichText(
                f'<p><a href="{tag_index.url}">View DICOM Tag Frequencies</a></p>'
            )))
            home_page.save()

        return site, home_page  

    def create_footer_menus(self, site):
        FlatMenu.objects.all().delete()

        # For some reason (possibly because contact-us is a form, not a page), the contact us never gets
        # rendered. So I'm rendering it manually in footer.html.
        #
        # Leaving this code in here in case we want to revisit it:
        #
        # contact = FlatMenu(site=site, title='1: Contact', handle='footer-contact', heading='Contact')
        # contact.save()
        # contact_page = Page.objects.filter(slug='contact-us').first()
        # FlatMenuItem(menu=contact, link_page=contact_page, link_text='Contact Us').save()
        # FlatMenuItem(
        #     menu=contact, link_url='https://www.jpl.nasa.gov/who-we-are/media-information/jpl-media-contacts',
        #     link_text='JPL Media Contacts'
        # ).save()

        # Examples of other footer menus:
        #
        # science = FlatMenu(site=site, title='2: Science', handle='footer-science', heading='Science')
        # science.save()
        # for slug in ('initiatives', 'technologies', 'workshops'):
        #     page = Page.objects.filter(slug=slug).first()
        #     FlatMenuItem(menu=science, link_page=page).save()
        #
        # info = FlatMenu(site=site, title='3: Information', handle='footer-info', heading='More Information')
        # info.save()
        # for slug in ('news', 'people'):
        #     page = Page.objects.filter(slug=slug).first()
        #     FlatMenuItem(menu=info, link_page=page).save()

        social = FlatMenu(site=site, title='4: Social Media', handle='footer-social', heading='Social Media')
        social.save()
        for url, text in (
            ('https://www.facebook.com/NASAJPL', 'Facebook'),
            ('https://www.youtube.com/user/JPLnews', 'YouTube'),
            ('https://www.instagram.com/nasajpl/', 'Instagram')
        ):
            FlatMenuItem(menu=social, link_url=url, link_text=text).save()

    def set_initial_settings(self, site):
        footer = Footer.objects.get_or_create(site_id=site.id)[0]
        footer.site_manager = 'Ashish Mahabal'
        footer.webmaster = 'Sean Kelly'
        footer.clearance = 'N/A'
        footer.save()

    def handle(self, *args, **options):
        self.stdout.write('Blooming "Dicominator" site')

        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False

            site, home_page = self.set_site(options['hostname'], options['port'])
            self.create_footer_menus(site)
            self.set_initial_settings(site)

            # self._set_settings(site)

        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
