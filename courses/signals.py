from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseTopic, Course
import json

@receiver(post_save, sender=CourseTopic)
def update_course_content(sender, instance, **kwargs):
    course = instance.course_chapter.course

    course_hierarchy = []
    for chapter in course.chapters.all():
        chapter_data = {
            'chapter_name': chapter.title,
            'lessons': [{'lesson_name': CourseTopic.title, 'lesson_id': CourseTopic.id} for topic in chapter.CourseTopic.all()]
        }
        course_hierarchy.append(chapter_data)

    course.course_content = course_hierarchy
    course.save()

@receiver(post_save, sender=Course)
def update_course_card_json(sender, instance, created, **kwargs):
    course_card_data = {
        "course_id": instance.course_id,
        "title": instance.title,
        "course_url": instance.course_url,
        "course_image": instance.course_image.url if instance.course_image else None,
        "price": str(instance.price) if instance.price else None,
        "short_description": instance.short_description,
        "author": "",#instance.author.username,
        "language": instance.language,
        "preview_video": instance.preview_video,
        "course_category": instance.course_category.name if instance.course_category else None,
    }
    
    if (course_card_data != instance.course_card_json):
        instance.course_card_json = course_card_data
        instance.save(update_fields=["course_card_json"])
