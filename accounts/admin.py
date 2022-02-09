from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'uuid', 'username', 'email', 'phone_number',
        'telegram_id', 'is_staff', 'is_active', 'last_login'
    )
    list_display_links = ('id', 'uuid', 'username')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ('password',)