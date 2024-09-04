from django.apps import AppConfig


class BuzzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buzz'

    def ready(self):
        import buzz.signals  # Import signals to ensure they are connected when the app is ready

'''
ready() method: This method is used to import the buzz.signals module, 
ensuring the signal is connected when the buzz app is loaded.
'''