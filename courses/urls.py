from django.urls import path
from .views import PublishedCourseCardsView, CourseOverviewAPIView


urlpatterns = [
    path('coursecards/', PublishedCourseCardsView.as_view(), name='coursecardapi'),
    path('<slug:slug>', CourseOverviewAPIView.as_view(), name='courseoverviewapi'),
]