from django.contrib import admin
from .models import (
    BlogCategory, BlogTag, Blog,
    BlogTagMapping, BlogCategoryMapping
)

"""
class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1
"""

class BlogTagMappingInline(admin.TabularInline):
    model = BlogTagMapping
    extra = 1


class BlogCategoryMappingInline(admin.TabularInline):
    model = BlogCategoryMapping
    extra = 1


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('blog_category_name', 'blog_category_slug', 'blog_category_created_at')
    prepopulated_fields = {"blog_category_slug": ("blog_category_name",)}
    search_fields = ('blog_category_name',)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('blog_tag_name', 'blog_tag_slug', 'blog_tag_created_at')
    prepopulated_fields = {"blog_tag_slug": ("blog_tag_name",)}
    search_fields = ('blog_tag_name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_slug', 'blog_status', 'blog_author', 'blog_category', 'blog_reading_time', 'blog_published_at')
    list_filter = ('blog_status', 'blog_category', 'blog_author')
    search_fields = ('blog_title', 'blog_snippet')
    prepopulated_fields = {"blog_slug": ("blog_title",)}
    readonly_fields = ('blog_reading_time', 'blog_created_at', 'blog_updated_at')
    inlines = [BlogTagMappingInline, BlogCategoryMappingInline]
    
    def display_tags(self, obj):
        return ", ".join(tag.blog_tag_name for tag in obj.blog_tags.all())
    display_tags.short_description = 'Tags'

"""
@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'blog_section_image', 'blog_section_video_url')
    search_fields = ('blog__blog_title',)
"""

@admin.register(BlogTagMapping)
class BlogTagMappingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'tag')
    search_fields = ('blog__blog_title', 'tag__blog_tag_name')


@admin.register(BlogCategoryMapping)
class BlogCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'category')
    search_fields = ('blog__blog_title', 'category__blog_category_name')
