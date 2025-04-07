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
    blog_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_category_name = models.CharField(max_length=100, unique=True)
    blog_category_slug = models.SlugField(unique=True, blank=True)
    blog_category_created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.blog_category_slug:
            self.blog_category_slug = slugify(self.blog_category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_category_name

class BlogTag(models.Model):
    blog_tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_tag_name = models.CharField(max_length=100, unique=True)
    blog_tag_slug = models.SlugField(unique=True, blank=True)
    blog_tag_created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.blog_tag_slug:
            self.blog_tag_slug = slugify(self.blog_tag_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_tag_name

class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    blog_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_title = models.CharField(max_length=200)
    blog_slug = models.SlugField(unique=True, blank=True)
    blog_snippet = CKEditor5Field('Excerpt', config_name='extends',null=True, blank=True)
    blog_snippet_json = models.JSONField(blank=True, null=True)
    blog_content = CKEditor5Field('Content', config_name='extends',null=True, blank=True)
    blog_content_json = models.JSONField(blank=True, null=True)
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    blog_tags = models.ManyToManyField(BlogTag, through='BlogTagMapping')
    blog_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    blog_seo_title = models.CharField(max_length=200, blank=True)
    blog_seo_description = models.TextField(blank=True)
    blog_seo_keywords = models.CharField(max_length=255, blank=True)
    blog_featured_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    blog_created_at = models.DateTimeField(default=timezone.now, blank=True)
    blog_updated_at = models.DateTimeField(default=timezone.now, blank=True)
    blog_published_at = models.DateTimeField(default=timezone.now, blank=True)
    blog_reading_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.blog_slug:
            self.blog_slug = slugify(self.blog_title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.blog_title

"""class BlogSection(models.Model):
    blog_section_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="sections")
    blog_section_content = CKEditor5Field('Content', config_name='extends',null=True, blank=True)
    blog_section_image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    blog_section_image_alt = models.CharField(max_length=255, null=True, blank=True)
    blog_section_video_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Section of {self.blog.blog_title}"
"""

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
    text = strip_tags(instance.blog_content)
    words = re.findall(r'\b\w+\b', text)
    instance.blog_reading_time = max(1, math.ceil(len(words) / 200)) 
    Blog.objects.filter(pk=instance.pk).update(blog_reading_time=instance.blog_reading_time)

"""
@receiver(post_save, sender=Blog)
def process_blog_content(sender, instance, **kwargs):
    combined_content = ""
    for section in instance.sections.all():
        if section.blog_section_content:
            combined_content += f"{section.blog_section_content}"
        if section.blog_section_image:
            combined_content += f'<img src="{section.blog_section_image.url}" alt="{section.blog_section_image_alt or ""}">'
        if section.blog_section_video_url:
            combined_content += f'<video src="{section.blog_section_video_url}" controls></video>'

    new_content_json = html_to_json(combined_content)
    new_snippet_json = html_to_json(instance.blog_snippet)
    
    if instance.blog_snippet_json != new_snippet_json:
        def update_snippet():
            instance.blog_snippet_json = new_snippet_json
            instance.save(update_fields=['blog_snippet_json'])
        transaction.on_commit(update_snippet)

    if instance.blog_content_json != new_content_json:
        def update_content():
            instance.blog_content_json = new_content_json
            instance.save(update_fields=['blog_content_json'])

        transaction.on_commit(update_content)
"""