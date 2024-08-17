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
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы"""

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

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
