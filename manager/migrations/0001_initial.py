# Generated by Django 5.1.1 on 2024-10-14 13:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chapter_name", models.CharField(max_length=100)),
                ("chapter_video", models.FileField(upload_to="course_videos/")),
            ],
        ),
        migrations.CreateModel(
            name="ChapterCompleted",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("completed", models.BooleanField(default=False)),
                (
                    "chapter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.chapter",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course_name", models.CharField(max_length=100)),
                ("price", models.IntegerField()),
                (
                    "trainer",
                    models.ForeignKey(
                        limit_choices_to={"profile__type": "TRAINER"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chapter",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="manager.course"
            ),
        ),
    ]
