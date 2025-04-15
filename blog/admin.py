from django.contrib import admin
from .models import (
    BlogCategory, BlogTag, Blog,
    BlogTagMapping, BlogCategoryMapping
)

class BlogTagMappingInline(admin.TabularInline):
    model = BlogTagMapping
    extra = 1


class BlogCategoryMappingInline(admin.TabularInline):
    model = BlogCategoryMapping
    extra = 1


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'author', 'category', 'reading_time', 'published_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'snippet')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('reading_time', 'published_at', 'updated_at')
    inlines = [BlogTagMappingInline, BlogCategoryMappingInline]
    
    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

"""
@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'section_image', 'section_video_url')
    search_fields = ('_title',)
"""

@admin.register(BlogTagMapping)
class BlogTagMappingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'tag')
    search_fields = ('title', 'tag__name')


@admin.register(BlogCategoryMapping)
class BlogCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('blog', 'category')
    search_fields = ('title', 'category__name')
