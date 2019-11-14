from rest_framework import serializers
from rest_framework.serializers import Serializer

from feedback.models import Feedback


class FeedbackSerializer(Serializer):
    submitted = serializers.DateTimeField()
    username = serializers.CharField()
    type = serializers.ChoiceField(Feedback.CHOICES)
    description = serializers.CharField()