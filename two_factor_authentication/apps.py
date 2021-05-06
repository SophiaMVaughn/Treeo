from django.apps import AppConfig


class TwoFactorAuthenticationConfig(AppConfig):
    name = 'two_factor_authentication'
    def ready(self):
        import upload_download.signals
