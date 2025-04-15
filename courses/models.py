from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
import uuid

User = get_user_model()

class CourseCategory(models.Model):
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


class Course(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    cover_image_alt = models.CharField(max_length=255, blank=True, null=True)
    preview_video = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, null=True, decimal_places=2)
    short_description = CKEditor5Field('Short Description', config_name='extends',null=True, blank=True)
    long_description = CKEditor5Field('Long Description', config_name='extends',null=True, blank=True)
    learning_outcomes = CKEditor5Field('Learning Outcomes', config_name='extends',null=True, blank=True)
    pre_requisites = CKEditor5Field('Pre Requisites', config_name='extends',null=True, blank=True)
    target_audience = CKEditor5Field('Who Is The Course For', config_name='extends',null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructors')
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=50, default="English")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now, blank=True)
    course_structure = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CourseChapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', db_index=True)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(help_text="Order of the chapter in the course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title}"
        
class CourseTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='topics', db_index=True)
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True, help_text="Optional video link for the course topic")
    content = CKEditor5Field('Content', config_name='extends', null=True, blank=True)
    order = models.PositiveIntegerField(help_text="Order of the topics in the chapter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"

class CourseCategoryMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('course', 'category')
        
class CourseQuiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='chapters', db_index=True)
    title = models.CharField(max_length=200)
    json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE, related_name='chapters', db_index=True)
    question = models.CharField(max_length=250)

class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='questions', db_index=True)
    option = models.CharField(max_length=255)

class QuestionAnswerMapping(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, db_index=True)
    answer = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, db_index=True)

class CourseEnrolled(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'user')