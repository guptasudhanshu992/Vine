from rest_framework import serializers
from .models import Course, CourseCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['course_category_id', 'course_category_name']
        
class CourseSerializer(serializers.ModelSerializer):
    course_category = CategorySerializer(CourseCategory.objects.all(), many=False)

    class Meta:
        model = Course
        fields = [
            "course_title",
            "course_url",
            "course_image",
            "course_price",
            "course_short_description",
            "course_long_description",
            "course_learning_outcomes",
            "course_pre_requisites",
            "course_content_json",
            "course_language",
            "course_preview_video",
            "course_category",
            "course_updated_at",
            "course_published_at"
        ]