from django.urls import path
from . import views

from .views import submit_feedback, view_feedback, reply_feedback, delete_feedback, my_feedbacks
from .views import recsubmit_feedback, recmy_feedbacks

urlpatterns = [
 path('studentuser_forgot_password.html', views.studentuser_forgot_password, name='studentuser_forgot_password'),
    path('recruiter_forgot_password.html/', views.recruiter_forgot_password, name='recruiter_forgot_password'),
    path('reset-password/<str:role>/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),


    path("submit_feedback/", submit_feedback, name="submit_feedback"),
    path("view_feedback/", view_feedback, name="view_feedback"),
    path("reply_feedback/<int:fid>/", reply_feedback, name="reply_feedback"),
    path("delete_feedback/<int:fid>/", delete_feedback, name="delete_feedback"),
    path("my_feedbacks/", my_feedbacks, name="my_feedbacks"),

    path("recsubmit_feedback/", recsubmit_feedback, name="recsubmit_feedback"),

    path("recmy_feedbacks/", recmy_feedbacks, name="recmy_feedbacks"),
]
