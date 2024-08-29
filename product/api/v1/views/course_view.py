from api.v1.permissions import (
    IsStudentOrIsAdmin,
    ReadOnlyOrIsAdmin,
    make_payment,
)
from api.v1.serializers.course_serializer import (
    CourseSerializer,
    CreateCourseSerializer,
    CreateGroupSerializer,
    CreateLessonSerializer,
    GroupSerializer,
    LessonSerializer,
)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from django.contrib.auth import get_user_model
from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    Value,
)
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(
            Course,
            id=self.kwargs.get("course_id"),
        )
        groups = course.groups.prefetch_related("students").annotate(
            students_count=Count("students")
        )
        return groups


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы"""

    queryset = Course.objects.prefetch_related("lessons")
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Если пользователь без прав is_staff,
        # то исключаем курсы с флагом available=False
        if not self.request.user.is_staff:
            queryset = queryset.filter(available=True)
        # Исключаем курсы, которые текущий пользователь уже приобрел
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(
                subscriptions__student=self.request.user
            )
        # Добавление в запрос количества уроков на курсе
        queryset = queryset.annotate(
            lessons_count=Count("lessons", distinct=True)
        )
        # Добавление в запрос количества подписчиков на курс
        queryset = queryset.annotate(
            students_count=Count("subscriptions__student", distinct=True)
        )
        # Добавление в запрос процент заполнения групп
        queryset = queryset.annotate(
            groups_filled_percent=Coalesce(
                ExpressionWrapper(
                    Avg("groups__students") * Value(100) / Value(30),
                    output_field=IntegerField(),
                ),
                Value(0),
            )
        )
        # Добавление в запрос процент приобретения продукта
        queryset = queryset.annotate(
            demand_course_percent=ExpressionWrapper(
                F("students_count") * Value(100) / User.objects.count(),
                output_field=IntegerField(),
            )
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        course = get_object_or_404(Course, pk=pk)
        data = {"course": course.id, "student": request.user.id}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            make_payment(request, course)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=404)
