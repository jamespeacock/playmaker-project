from django.http import JsonResponse

# Create your views here.
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer
from playmaker.shared.views import SecureAPIView


class CreateFeedback(SecureAPIView):

    def post(self, request, *args, **kwargs):
        data = self.get_params(request.data, FeedbackSerializer)
        data['user']= request.user.username
        created = Feedback.objects.create(data)
        if created:
            return JsonResponse("Feedback submitted successfully.", safe=False)
