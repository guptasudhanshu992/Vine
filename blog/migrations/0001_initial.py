# Generated by Django 5.1.7 on 2025-04-07 04:25

import django.utils.timezone
import django_ckeditor_5.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "blog_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("blog_title", models.CharField(max_length=200)),
                ("blog_slug", models.SlugField(blank=True, unique=True)),
                (
                    "blog_snippet",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Text"
                    ),
                ),
                ("blog_snippet_json", models.JSONField(blank=True, null=True)),
                ("blog_content_json", models.JSONField(blank=True, null=True)),
                (
                    "blog_status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("published", "Published")],
                        default="draft",
                        max_length=10,
                    ),
                ),
                ("blog_seo_title", models.CharField(blank=True, max_length=200)),
                ("blog_seo_description", models.TextField(blank=True)),
                ("blog_seo_keywords", models.CharField(blank=True, max_length=255)),
                (
                    "blog_featured_image",
                    models.ImageField(blank=True, null=True, upload_to="static/blogs/"),
                ),
                (
                    "blog_created_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "blog_updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "blog_published_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("blog_reading_time", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "blog_category_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("blog_category_name", models.CharField(max_length=100, unique=True)),
                ("blog_category_slug", models.SlugField(blank=True, unique=True)),
                ("blog_category_created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="BlogCategoryMapping",
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
                    "blog_section_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "blog_section_content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Content"
                    ),
                ),
                (
                    "blog_section_image",
                    models.ImageField(blank=True, null=True, upload_to="blogs/"),
                ),
                (
                    "blog_section_image_alt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "blog_section_video_url",
                    models.URLField(blank=True, max_length=500, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlogTag",
            fields=[
                (
                    "blog_tag_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("blog_tag_name", models.CharField(max_length=100, unique=True)),
                ("blog_tag_slug", models.SlugField(blank=True, unique=True)),
                ("blog_tag_created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="BlogTagMapping",
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
    ]
