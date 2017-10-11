from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import InvitationCode

class InvitationCodeAdmin(admin.ModelAdmin):
    fields = ('code', 'limit_mobile', 'limit_count', 'expire_seconds')
    list_display = ('code', 'limit_mobile', 'limit_count', 'used_count', 'used_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id)

    def save_model(self, request, obj, form, change):
        obj.user_id = request.user.id
        super(InvitationCodeAdmin, self).save_model(request, obj, form, change)

admin.site.register(InvitationCode, InvitationCodeAdmin)

