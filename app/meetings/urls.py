from django.urls import path
from . import views
from .views import CourseMeetingListView


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'), # search course (student)
    path('dashboard/', views.dashboard, name='dashboard'), # dashboard (same for all users)
    path('course_meetings/<int:course_id>/', CourseMeetingListView.as_view(), name='course_meetings'), # search meetings (student)
    path('search_tutor/', views.search_tutor, name='search_tutor'), # search course (tutor)
    path('search_tutor/schedule/<int:course_id>', views.schedule, name='schedule'), # create meeting (tutor),
    path('schedule_meeting/<int:meeting_id>', views.schedule_meeting, name='schedule_meeting'),
    path('delete_meeting/<int:meeting_id>', views.delete_meeting, name='delete_meeting'),
    path('review_meeting/<int:meeting_id>', views.review_meeting, name='review_meeting')
]
