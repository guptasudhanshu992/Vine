# Generated by Django 5.1.7 on 2025-05-08 06:43

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="BlogTag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "cover_image",
                    models.ImageField(blank=True, null=True, upload_to="blogs/"),
                ),
                (
                    "snippet",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Excerpt"
                    ),
                ),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        blank=True, null=True, verbose_name="Content"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("draft", "Draft"), ("published", "Published")],
                        default="Draft",
                        max_length=10,
                    ),
                ),
                ("seo_title", models.CharField(blank=True, max_length=200)),
                ("seo_description", models.TextField(blank=True)),
                ("seo_keywords", models.CharField(blank=True, max_length=255)),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "published_at",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                ("reading_time", models.PositiveIntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
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
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.blog"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.blogcategory",
                    ),
                ),
            ],
            options={
                "unique_together": {("blog", "category")},
            },
        ),
        migrations.AddField(
            model_name="blog",
            name="categories",
            field=models.ManyToManyField(
                through="blog.BlogCategoryMapping", to="blog.blogcategory"
            ),
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
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.blog"
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.blogtag"
                    ),
                ),
            ],
            options={
                "unique_together": {("blog", "tag")},
            },
        ),
        migrations.AddField(
            model_name="blog",
            name="tags",
            field=models.ManyToManyField(
                through="blog.BlogTagMapping", to="blog.blogtag"
            ),
        ),
    ]
