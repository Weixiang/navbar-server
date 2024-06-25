from django.apps import AppConfig


class NavsysmainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "navsysMain"
    verbose_name = '仓储管理'

    def ready(self):
        import navsysMain.handlers
