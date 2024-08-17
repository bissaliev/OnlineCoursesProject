from django.db.models import F
from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import Subscription


def make_payment(request, course):
    request.user.balance.bonus = F("bonus") - course.price
    request.user.balance.save()
    request.user.balance.refresh_from_db()


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return Subscription.objects.filter(
            student=request.user, course__id=view.kwargs.get("course_id")
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return Subscription.objects.filter(
            student=request.user, course__lessons=obj
        ).exists()


class ReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
