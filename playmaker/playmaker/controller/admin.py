from django.contrib import admin

from playmaker.controller.models import Controller, Listener, Group, Permission, Queue, SongInQueue


class ControllerAdmin(admin.ModelAdmin):
    pass


class ListenerAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    model = Group
    # fields = ('get_group', 'get_listeners')

    def get_group(self, obj):
        return 'Group {} hosted by {}'.format(obj.id, obj.controller.me.username)
    get_group.short_description = 'Group'  # Allows column order sorting

    def get_listeners(self, obj):
        return [l.me.username for l in obj.listeners.all()]
    get_listeners.short_description = 'Listeners'  #Renames column head


class PermissionAdmin(admin.ModelAdmin):
    pass


class SongInQueueInline(admin.TabularInline):
    model = SongInQueue


class QueueAdmin(admin.ModelAdmin):
    model = Queue
    inlines = [SongInQueueInline]

    def get_songs(self, obj):
        return [song.name for song in obj.songs.all()]
    get_songs.short_description = 'Queued songs'


admin.site.register(Controller, ControllerAdmin)
admin.site.register(Listener, ListenerAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Queue, QueueAdmin)