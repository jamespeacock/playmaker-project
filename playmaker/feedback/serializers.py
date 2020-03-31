from rest_framework import serializers
from rest_framework.serializers import Serializer

from feedback.models import Feedback


class FeedbackSerializer(Serializer):
    type = serializers.ChoiceField(Feedback.CHOICES, required=True)
    description = serializers.CharField(required=True)