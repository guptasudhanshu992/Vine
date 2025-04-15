from django.contrib import admin
from .models import (
    CourseCategory, Course, CourseCategoryMapping,
    CourseChapter, CourseTopic, CourseQuiz,
    QuizQuestion, QuestionOption, QuestionAnswerMapping,
    CourseEnrolled
)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'language', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'language')
    search_fields = ('title',)


@admin.register(CourseCategoryMapping)
class CourseCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('course','category')


@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title',)


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order', 'created_at')
    list_filter = ('chapter',)
    search_fields = ('title',)


@admin.register(CourseQuiz)
class CourseQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'question')


@admin.register(QuestionAnswerMapping)
class QuestionAnswerMappingAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(CourseEnrolled)
class CourseEnrolledAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'created_at')
    list_filter = ('course',)
