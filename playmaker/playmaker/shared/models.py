from django.db import models


class SPModel(models.Model):
    sp_id = models.CharField(max_length=255)
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
        data = spotify_resp[cls.get_key()]

        if query:
            # Is it necessary to serialize this into an object just for querying? 
            # data = [cls.from_sp(save=save, **item) for item in data['items']]
            l = [] if serializer else data['items']
            if not l:
                for d in data['items']:
                    ser_d = serializer(d)
                    l.append(ser_d.data)
            return {cls.get_key(): l,
                    "next": data['next']}
        else:
            if save:
                return [cls.from_sp(save=save, **obj) for obj in data]
            return [serializer(d).data if serializer else d for d in data]