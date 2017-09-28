from pelican import signals


def set_settings(pelican_obj):
    is_testing = pelican_obj.settings.get('TESTING', False)
    if is_testing:
        pelican_obj.settings['DIRECT_TEMPLATES'].append('drafts')
        pelican_obj.settings['PAGINATED_DIRECT_TEMPLATES'].append('drafts')


def register():
    signals.initialized.connect(set_settings)
