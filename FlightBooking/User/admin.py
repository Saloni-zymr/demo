from .models import User, Passenger, BookingDetails, Flight
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', "name", "email", "is_staff", "is_admin")
    list_filter = ("is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "name",
                    "address",
                    "last_login",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        # (
        #     # "Permissions",
        #     # {"fields": ("groups", "user_permissions")},
        # ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "address",
                    "contact",
                    "gender",
                    # "city",
                    "age",
                    # "state",
                    # "country",
                    # "pincode",
                    "password1",
                    "password2",
                    "is_active",
                    # "is_admin",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email", 'id')
    filter_horizontal = ()


admin.site.register([Passenger, BookingDetails, Flight])
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
