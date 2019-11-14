from django.urls import path
from feedback.views import CreateFeedback


urlpatterns = [
    path('', CreateFeedback.as_view(), name="create-feedback"),
]
