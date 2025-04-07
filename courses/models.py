from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
import uuid

User = get_user_model()

class CourseCategory(models.Model):
    course_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_category_name = models.CharField(max_length=100, unique=True)
    course_category_slug = models.SlugField(unique=True, blank=True)
    course_category_created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.course_category_slug:
            self.course_category_slug = slugify(self.course_category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_category_name
        
class Course(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_title = models.CharField(max_length=200, unique=True)
    course_url = models.SlugField(max_length=200, unique=True, blank=True)
    course_image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    course_image_alt = models.CharField(max_length=255, blank=True, null=True)
    course_price = models.DecimalField(max_digits=8, null=True, decimal_places=2)
    course_short_description = CKEditor5Field('Short Description', config_name='extends',null=True, blank=True)
    course_long_description = CKEditor5Field('Long Description', config_name='extends',null=True, blank=True)
    course_learning_outcomes = CKEditor5Field('Learning Outcomes', config_name='extends',null=True, blank=True)
    course_pre_requisites = CKEditor5Field('Pre Requisites', config_name='extends',null=True, blank=True)
    course_target_audience = CKEditor5Field('Who Is The Course For', config_name='extends',null=True, blank=True)
    course_author = models.ForeignKey(User, on_delete=models.CASCADE)
    course_language = models.CharField(max_length=50, default="English")
    course_preview_video = models.URLField(blank=True, null=True)
    course_card_json = models.JSONField(blank=True, null=True)
    course_overview_json = models.JSONField(blank=True, null=True)
    course_content_json = models.JSONField(blank=True, null=True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, db_index=True)
    course_created_at = models.DateTimeField(auto_now_add=True)
    course_updated_at = models.DateTimeField(auto_now=True)
    course_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    course_published_at = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.course_url:
            self.course_url = slugify(self.course_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_title

class CourseCategoryMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('course', 'course_category')
        
class CourseChapter(models.Model):
    course_chapter_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters', db_index=True)
    course_chapter_title = models.CharField(max_length=200)
    course_chapter_order = models.PositiveIntegerField(help_text="Order of the chapter in the course")
    course_chapter_created_at = models.DateTimeField(auto_now_add=True)
    course_chapter_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_chapter_order']

    def __str__(self):
        return f"{self.course_chapter_title} - {self.course.course_title}"

class CourseTopic(models.Model):
    course_topic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='lessons', db_index=True)
    course_topic_title = models.CharField(max_length=200)
    course_topic_content = CKEditor5Field('Text', config_name='extends',null=True, blank=True)
    course_topic_order = models.PositiveIntegerField(help_text="Order of the topics in the chapter")
    course_topic_video_url = models.URLField(blank=True, null=True, help_text="Optional video link for the course topic")
    course_topic_created_at = models.DateTimeField(auto_now_add=True)
    course_topic_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_topic_order']

    def __str__(self):
        return f"{self.course_topic_title} - {self.chapter.course_chapter_title}"

class CourseQuiz(models.Model):
    course_quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_quiz_title = models.CharField(max_length=200)
    course_quiz_json = models.JSONField(blank=True, null=True)
    course_quiz_created_at = models.DateTimeField(auto_now_add=True)
    course_quiz_updated_at = models.DateTimeField(auto_now=True)

class QuizQuestion(models.Model):
    quiz_question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE, db_index=True)
    quiz_question = models.CharField(max_length=250)
    course_chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    course_topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, blank=True, null=True, db_index=True)

class QuestionOption(models.Model):
    question_option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, db_index=True)
    question_option = models.CharField(max_length=255)

class QuestionAnswerMapping(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, db_index=True)
    quiz_question_answer = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, db_index=True)

class CourseEnrolled(models.Model):
    course_enrollment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    course_enrolled_user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course_enrolled_created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'course_enrolled_user')