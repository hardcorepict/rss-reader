import factories as f

from mail.services import Template
from mail.tasks import send_mail


def test_send_mail(celery_worker):

    email = "test@test.com"
    mail = f.MailFactory(
        template=Template.WELCOME,
        recipients=[email],
    )
    send_mail.delay(mail)
