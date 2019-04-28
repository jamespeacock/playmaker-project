from django.contrib import admin

from playmaker.songs.models import Song


class SongAdmin(admin.ModelAdmin):
    pass


admin.site.register(Song, SongAdmin)
