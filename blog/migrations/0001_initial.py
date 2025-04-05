# Generated by Django 5.1.7 on 2025-04-05 08:31

import django.utils.timezone
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                ("blog_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "snippet",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Text"
                    ),
                ),
                ("snippet_json", models.JSONField(blank=True, null=True)),
                ("content_json", models.JSONField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("published", "Published")],
                        default="draft",
                        max_length=10,
                    ),
                ),
                ("seo_title", models.CharField(blank=True, max_length=200)),
                ("seo_description", models.TextField(blank=True)),
                ("seo_keywords", models.CharField(blank=True, max_length=255)),
                (
                    "featured_image",
                    models.ImageField(blank=True, null=True, upload_to="static/blogs/"),
                ),
                (
                    "created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "published_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("reading_time", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="BlogCategory",
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
            ],
        ),
        migrations.CreateModel(
            name="BlogSection",
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
                (
                    "content_text",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Text"
                    ),
                ),
                (
                    "section_image",
                    models.ImageField(blank=True, null=True, upload_to="blogs/"),
                ),
                (
                    "section_image_alt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "section_video_url",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlogTag",
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
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("category_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("tag_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
