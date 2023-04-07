from django.contrib import admin
from .models import Outbound


@admin.register(Outbound)
class OutboundAdmin(admin.ModelAdmin):
    pass
