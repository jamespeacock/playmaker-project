from django.db import models


class SPModel(models.Model):
    sp_id = models.CharField(max_length=255, unique=True)
    href = models.CharField(max_length=511)

    @staticmethod
    def pop_kwargs(kwargs):
        kwargs['sp_id'] = kwargs.pop('id')
        return kwargs

    @staticmethod
    def from_sp(kwargs):
        return SPModel.pop_kwargs(kwargs)

    @staticmethod
    def from_response(spotify_resp, cls, save=False, serializer=None, query=False):
        response_data = spotify_resp[cls.get_key()]

        if query:
            data = [cls.from_sp(save=save, **item) for item in response_data['items']]
            return {cls.get_key(): [serializer(d).data if serializer else d for d in data],
                    "next": response_data['next']}
        data = [cls.from_sp(save=save, **obj) for obj in response_data]
        return [serializer(d).data if serializer else d for d in data]