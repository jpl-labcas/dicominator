# encoding: utf-8

'''📜 Dicominator content: settings.'''


# Migration Modules
#
# This shouldn't be necessary, but I am seeing the generated migrations code end up in the virtual
# environment and not in the source tree when running `makemigrations` 🤨
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules

MIGRATION_MODULES = {
    'jpl.labcas.dicominator.content': 'jpl.labcas.dicominator.content.migrations'
}


# Installed Applications
# ----------------------
#
# The "apps" (Python packages) enabled for Django.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps

INSTALLED_APPS = [
    # 'widget_tweaks',  # Not used at this time
]
