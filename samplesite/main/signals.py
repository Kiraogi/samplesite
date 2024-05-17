from django.dispatch import Signal, receiver

from .utilities import send_activation_notification

post_register = Signal()


@receiver(post_register)
def post_register_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
