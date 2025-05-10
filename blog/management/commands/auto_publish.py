from django.core.management.base import BaseCommand
from django.utils.timezone import now
from blog.models import Blog 
from core.models import CronJobExecutionLog


class Command(BaseCommand):
    help = 'Auto-publish blogs that are scheduled for the current time'

    def handle(self, *args, **kwargs):
        blogs = Blog.objects.filter(status='Draft', published_at__lte=now())
        updated_count = 0

        for blog in blogs:
            blog.status = 'Published'
            blog.save()
            updated_count += 1

        # Log this execution
        CronJobExecutionLog.objects.create(
            job_name='auto_publish',
        )

        self.stdout.write(self.style.SUCCESS(f'{updated_count} blog(s) published and cron execution logged.'))
