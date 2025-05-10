from rest_framework import serializers
from .models import Blog, BlogCategory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BlogCategory.objects.all(),
        required=False
    )

    author = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'title', 
            'slug', 
            'snippet',
            'author', 
            'category', 
            'cover_image', 
            'updated_at',
            'published_at',
            'reading_time'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name']

class BlogDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BlogCategory.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'snippet',
            'content',
            'updated_at',
            'reading_time',
            'category',
        ]
