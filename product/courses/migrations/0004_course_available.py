# Generated by Django 4.2.10 on 2024-08-17 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_course_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="available",
            field=models.BooleanField(default=False, verbose_name="Доступен"),
        ),
    ]
