from django.urls import path
from exams import views
app_name = 'exams'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('exam/<int:exam_id>', views.ExamSolutionView.as_view(), name='exam_solution'),
    path('create/', views.ExamCreateView.as_view(), name='create'),
    path('api/get_subjects', views.GetSubjectsAPIView.as_view(), name='get_subjects'),
    path('api/create_exam', views.CreateExamAPIView.as_view(), name='create_exam'),
]
