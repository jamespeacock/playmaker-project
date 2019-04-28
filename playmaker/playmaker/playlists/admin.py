from django.contrib import admin

from playmaker.playlists.models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    pass


admin.site.register(Playlist, PlaylistAdmin)
