from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Balance, CustomUser


@receiver(post_save, sender=CustomUser)
def post_save_subscription(sender, instance: CustomUser, created, **kwargs):
    """
    Создание баланса при регистрации пользователя.
    """
    if created:
        Balance.objects.create(student=instance)
