from django.urls import path
from .views import FeedbackFormView, SuccessView


urlpatterns = [
    path('feedback/', FeedbackFormView.as_view(), name="feedback_form"),
    path('success/', SuccessView.as_view(), name="success_view"),
]
