from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Personal", {"fields": ("name",)}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ("last_login",)
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    add_form_template = "admin/auth/user/add_form.html"
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "name")
    filter_horizontal = ()
    list_per_page = 20
    def get_fieldsets(self, request, obj=None):
        """Return the fieldsets for the user change form."""
        if obj:
            return super().get_fieldsets(request, obj)
        return self.add_fieldsets
    def get_readonly_fields(self, request, obj=None):
        """Return the readonly fields for the user change form."""
        if obj:
            return self.readonly_fields
        return []


admin.site.register(models.User, UserAdmin)
