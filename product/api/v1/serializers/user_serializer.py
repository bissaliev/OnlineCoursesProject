from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    balance = serializers.ReadOnlyField(source="balance.bonus")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "last_name",
            "first_name",
            "email",
            "balance",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    class Meta:
        model = Subscription
        fields = (
            "course",
            "student",
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("course", "student"),
                message="Вы уже подписаны на данный курс.",
            )
        ]

    def validate(self, attrs):
        """
        Проверяем что у пользователя достаточно бонусов для подписки на курс.
        """
        course = attrs.get("course")
        student = attrs.get("student")
        if student.balance.bonus < course.price:
            raise serializers.ValidationError(
                "У вас недостаточно бонусов для подписки на этот курс."
            )
        return attrs
