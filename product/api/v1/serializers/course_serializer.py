from courses.models import Course, Group, Lesson
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = ("title", "link", "course")


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = ("title", "link", "course")


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    course = serializers.StringRelatedField(read_only=True)
    students_count = serializers.ReadOnlyField()
    students = StudentSerializer(many=True)

    class Meta:
        model = Group
        fields = ("id", "title", "course", "students_count", "students")


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = ("title",)


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = ("title",)


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.ReadOnlyField()
    students_count = serializers.ReadOnlyField()
    groups_filled_percent = serializers.ReadOnlyField()
    demand_course_percent = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = (
            "id",
            "author",
            "title",
            "start_date",
            "price",
            "lessons_count",
            "lessons",
            "demand_course_percent",
            "students_count",
            "groups_filled_percent",
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = ("author", "title", "start_date", "price", "available")
