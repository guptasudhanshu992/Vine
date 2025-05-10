from django.shortcuts import render, get_object_or_404
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.filter(status='published').order_by('-published_at')
    return render(request, 'blog.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    return render(request, 'blog-details.html', {'blog': blog})
