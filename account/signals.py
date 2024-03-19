from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info("New instance of User created: %s", instance)
    else:
        logger.info("Instance of User updated: %s", instance)


@receiver(post_delete, sender=User)
def user_post_delete_handler(sender, instance, **kwargs):
    logger.info("Instance of User deleted: %s", instance)
