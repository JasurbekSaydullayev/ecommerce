from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def my_model_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info("New instance of Product created: %s", instance)
    else:
        logger.info("Instance of Product updated: %s", instance)


@receiver(post_delete, sender=Product)
def user_post_delete_handler(sender, instance, **kwargs):
    logger.info("Instance of Product deleted: %s", instance)
