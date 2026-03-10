from django.apps import AppConfig

class IproviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iprovider'

    def ready(self):
        import iprovider.signals # noqa