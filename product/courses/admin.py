from django.contrib import admin

from .models import Course, Group, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson


class GroupInline(admin.TabularInline):
    model = Group


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "available", "price", "start_date"]
    list_editable = ["available", "price", "start_date"]
    inlines = [LessonInline, GroupInline]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]
