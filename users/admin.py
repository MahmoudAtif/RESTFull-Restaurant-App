from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SecretToken, SendEmail
from .forms import CustomeUserCreationForm
# Register your models here.

# add is_blocked field to Permissions fieldset
fieldsets = list(UserAdmin.fieldsets)
fieldsets[2] = (
    'Permissions', {
        'fields': (
            "is_active",
            "is_staff",
            "is_superuser",
            'is_blocked',
            "groups",
            "user_permissions",
        )
    }
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'email', 'password1', 'password2',),
            },
        ),
    )
    add_form = CustomeUserCreationForm
    fieldsets = fieldsets


@admin.register(SecretToken)
class SecretTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(SendEmail)
class SendEmailAdmin(admin.ModelAdmin):
    pass
