from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog, BlogCategoryMapping, BlogTagMapping

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    ordering = ['-created_at']

class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    ordering = ['-created_at']

class BlogCategoryMappingInline(admin.TabularInline):
    model = BlogCategoryMapping
    extra = 1

class BlogTagMappingInline(admin.TabularInline):
    model = BlogTagMapping
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at', 'updated_at', 'reading_time')
    list_filter = ('status', 'published_at', 'updated_at', 'categories', 'tags')
    search_fields = ('title', 'author__username', 'seo_title', 'seo_description', 'seo_keywords')
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at']
    inlines = [BlogCategoryMappingInline, BlogTagMappingInline]
    fieldsets = (
        ("Blog Info", {
            'fields': ('title', 'slug', 'author', 'cover_image')
        }),
        ("Content", {
            'fields': ('snippet', 'content')
        }),
        ("Metadata", {
            'fields': ('status', 'published_at', 'updated_at', 'reading_time')
        }),
        ("SEO", {
            'fields': ('seo_title', 'seo_description', 'seo_keywords')
        }),
    )

admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogTag, BlogTagAdmin)
admin.site.register(Blog, BlogAdmin)
