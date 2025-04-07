from rest_framework import serializers
from .models import Blog, BlogCategory
from userauthentication.models import NewUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogSerializer(serializers.ModelSerializer):
    blog_category = serializers.SlugRelatedField(
        slug_field='blog_category_name',
        queryset=BlogCategory.objects.all(),
        required=False
    )

    blog_author = serializers.SlugRelatedField(
        slug_field='email',
        queryset=NewUser.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'blog_title', 
            'blog_slug', 
            'blog_snippet',
            'blog_snippet_json', 
            'blog_author', 
            'blog_category', 
            'blog_featured_image', 
            'blog_updated_at',
            'blog_published_at',
            'blog_reading_time'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['blog_category_name']

class BlogDetailSerializer(serializers.ModelSerializer):
    blog_category = serializers.SlugRelatedField(
        slug_field='blog_category_name',
        queryset=BlogCategory.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'blog_id',
            'blog_title',
            'blog_slug',
            'blog_snippet',
            'blog_content',
            'blog_content_json',
            'blog_updated_at',
            'blog_reading_time',
            'blog_category',
        ]
