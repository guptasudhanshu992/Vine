from django.db import models

class CronJobExecutionLog(models.Model):
    job_name = models.CharField(max_length=255)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_name} ran at {self.executed_at}"
