from django.contrib import admin
from .models import Organization, UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1  # Number of extra forms to show in the inline

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ('name', 'domains', 'created_date', 'updated_date')
    search_fields = ('name', 'domains')

admin.site.register(Organization, OrganizationAdmin)
