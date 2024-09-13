from django.contrib import admin
from .models import Organization, UserProfile

class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1 

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ('name', 'domains', 'created_date', 'created_by', 'updated_date')
    search_fields = ('name', 'domains')

admin.site.register(Organization, OrganizationAdmin)
