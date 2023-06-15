from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    
    def ready(self) -> None:
        import common.signals
        return super().ready()