from templated_email import send_templated_mail

from app import celery_app
from mail.services import Mail


@celery_app.task(serializer="pickle")
def send_mail(mail: Mail):
    send_templated_mail(
        template_name=mail.template,
        from_email=mail.sender,
        recipient_list=mail.recipients,
        context=mail.context,
    )
