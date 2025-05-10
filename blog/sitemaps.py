from django.contrib.sitemaps import Sitemap
from .models import Blog

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Blog.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.publish_time
