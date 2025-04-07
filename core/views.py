from django.shortcuts import render
from django.views import View
from userauthentication.mixins import RedirectAuthenticatedUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import Http404

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class BlogView(View):
    def get(self, request):
        return render(request, 'blog.html')

class BlogDetailsView(View):
    def get(self, request, slug):
        return render(request, 'blogdetails.html')

class CoursesView(View):
    def get(self, request):
        return render(request, 'courses.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class LoginView(RedirectAuthenticatedUserMixin, View):
    def get(self, request):
        return render(request, 'login.html')

class RegisterView(RedirectAuthenticatedUserMixin, View):
    def get(self, request):
        return render(request, 'register.html')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')

class CourseDetailsView(DetailView):
    def get(self, request, slug):
        return render(request, 'course_details.html')

class LessonView(DetailView):
    def get(self, request, slug):
        return render(request, 'course_details.html') 
        
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)