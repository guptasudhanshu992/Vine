from django.contrib import admin
from .models import (
    CourseCategory, Course, CourseCategoryMapping,
    CourseChapter, CourseTopic, CourseQuiz,
    QuizQuestion, QuestionOption, QuestionAnswerMapping,
    CourseEnrolled
)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('course_category_name', 'course_category_slug', 'course_category_created_at')
    prepopulated_fields = {'course_category_slug': ('course_category_name',)}
    search_fields = ('course_category_name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_status', 'course_language', 'course_created_at')
    prepopulated_fields = {'course_url': ('course_title',)}
    list_filter = ('course_status', 'course_language', 'course_category')
    search_fields = ('course_title',)


@admin.register(CourseCategoryMapping)
class CourseCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('course', 'course_category')


@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('course_chapter_title', 'course', 'course_chapter_order', 'course_chapter_created_at')
    list_filter = ('course',)
    search_fields = ('course_chapter_title',)


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('course_topic_title', 'course_chapter', 'course_topic_order', 'course_topic_created_at')
    list_filter = ('course_chapter',)
    search_fields = ('course_topic_title',)


@admin.register(CourseQuiz)
class CourseQuizAdmin(admin.ModelAdmin):
    list_display = ('course_quiz_title', 'course_quiz_created_at')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz_question', 'course_quiz', 'course_chapter', 'course_topic')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question_option', 'quiz_question')


@admin.register(QuestionAnswerMapping)
class QuestionAnswerMappingAdmin(admin.ModelAdmin):
    list_display = ('quiz_question', 'quiz_question_answer')


@admin.register(CourseEnrolled)
class CourseEnrolledAdmin(admin.ModelAdmin):
    list_display = ('course', 'course_enrolled_user', 'course_enrolled_created_at')
    list_filter = ('course',)
