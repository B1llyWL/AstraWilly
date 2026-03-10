from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_support_ticket_email(ticket_id, name, email, subject, message):
    """
    Асинхронная отправка email о новом тикете поддержки.
    """
    logger.info(f"Sending email for ticket #{ticket_id}")
    try:
        send_mail(
            subject=f"New support ticket: {subject}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
        logger.info(f"Email sent for ticket #{ticket_id}")
        return f"Email sent for ticket {ticket_id}"
    except Exception as e:
        logger.error(f"Failed to send email for ticket #{ticket_id}: {e}")
        raise e