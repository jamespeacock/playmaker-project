from django.contrib import admin

from playmaker.controller.models import Controller, Listener, Group, Device, Permission, Queue, SongInQueue


class ControllerAdmin(admin.ModelAdmin):
    pass


class ListenerAdmin(admin.ModelAdmin):
    pass


class ListenerInline(admin.TabularInline):
    model = Listener


class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = [ListenerInline]
    list_display = ['get_group', 'get_listeners']

    def get_group(self, obj):
        return 'Group {} hosted by {}'.format(obj.id, obj.controller.me.username)
    get_group.short_description = 'controller username'  # Allows column order sorting

    def get_listeners(self, obj):
        return [l.me.username for l in obj.listeners.all()]
    get_listeners.short_description = 'listener usernames'  #Renames column head


class DeviceAdmin(admin.ModelAdmin):
    pass


class PermissionAdmin(admin.ModelAdmin):
    pass


class QueueAdmin(admin.ModelAdmin):
    pass


class SongInQueueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Controller, ControllerAdmin)
admin.site.register(Listener, ListenerAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(SongInQueue, SongInQueueAdmin)