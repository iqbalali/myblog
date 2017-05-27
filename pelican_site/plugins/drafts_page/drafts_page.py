from pelican import signals
import os


def set_settings(pelican_obj):
    settings = pelican_obj.settings
    cwd = os.path.dirname(os.path.abspath(__file__))
    is_testing = settings.get('TESTING', False)
    if is_testing:
        settings['DIRECT_TEMPLATES'].append('drafts')
        settings['PAGINATED_DIRECT_TEMPLATES'].append('drafts')

def register():
    signals.initialized.connect(set_settings)
