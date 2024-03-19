from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderItem)
def order_item_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info("New instance of OrderItem created: %s", instance)
    else:
        logger.info("Instance of OrderItem updated: %s", instance)


@receiver(post_delete, sender=OrderItem)
def user_post_delete_handler(sender, instance, **kwargs):
    logger.info("Instance of OrderItem deleted: %s", instance)
