from django.core import serializers

from feedback.models import Feedback


class FeedbackSerializer(serializers.Serializer):

    class Meta:
        model = Feedback
        fields = ["submitted", "user", "type", "description"]