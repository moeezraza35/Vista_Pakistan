from django.core.mail.backends.smtp import EmailBackend
import ssl

class InsecureEmailBackend(EmailBackend):
    def _get_connection(self):
        self.connection = super()._get_connection()
        self.connection.context = ssl._create_unverified_context()
        return self.connection
