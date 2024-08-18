from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """

    if created:
        group = (
            Group.objects.filter(course=instance.course)
            .annotate(students_count=Count("students"))
            .order_by("students_count")
            .first()
        )
        group.students.add(instance.student)
