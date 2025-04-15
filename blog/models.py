from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from bs4 import BeautifulSoup
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import math
from django.db import transaction
from django_ckeditor_5.fields import CKEditor5Field
import uuid
import re
from django.utils.html import strip_tags

User = get_user_model()


def html_to_json(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')

    content = []
    stack = []

    def add_to_parent(element):
        if stack:
            parent = stack[-1]
            if 'content' not in parent:
                parent['content'] = []
            parent['content'].append(element)
        else:
            content.append(element)

    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img', 'video']):
        if element.name in ['h1', 'h2', 'h3']:
            level = int(element.name[1])

            while stack and int(stack[-1]['type'][1]) >= level:
                stack.pop()

            heading = {"type": element.name, "text": element.get_text(strip=True), "content": []}
            add_to_parent(heading)

            stack.append(heading)

        elif element.name == 'p':
            paragraph = {"type": "p", "text": element.get_text(strip=True)}
            add_to_parent(paragraph)

        elif element.name in ['img', 'video']:
            media = {
                "type": "image" if element.name == "img" else "video",
                "src": element.get('src'),
                "alt": element.get('alt', '') if element.name == "img" else '',
                "controls": element.has_attr('controls') if element.name == 'video' else None,
                "autoplay": element.has_attr('autoplay') if element.name == 'video' else None
            }
            add_to_parent(media)

    return json.dumps({"content": content}, separators=(',', ':'))


class BlogCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    cover_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    snippet = CKEditor5Field('Excerpt', config_name='extends',null=True, blank=True)
    content = CKEditor5Field('Content', config_name='extends',null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(BlogTag, through='BlogTagMapping')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    published_at = models.DateTimeField(default=timezone.now, blank=True)
    reading_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogTagMapping(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ForeignKey(BlogTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'tag')

class BlogCategoryMapping(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'category')

@receiver(post_save, sender=Blog)
def update_blogpost_word_count(sender, instance, **kwargs):
    text = strip_tags(instance.content)
    words = re.findall(r'\b\w+\b', text)
    instance.reading_time = max(1, math.ceil(len(words) / 200)) 
    Blog.objects.filter(pk=instance.pk).update(reading_time=instance.reading_time)