from django.contrib import admin
from .models import (
    Profile, Research, Publication, Project, Award, CVFile,
    ContactMessage, GalleryImage,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_image', 'about_preview')
    list_display_links = ('id',)

    def about_preview(self, obj):
        return (obj.about_text[:60] + '...') if obj.about_text and len(obj.about_text) > 60 else (obj.about_text or '-')

    about_preview.short_description = 'About'


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')


@admin.register(CVFile)
class CVFileAdmin(admin.ModelAdmin):
    list_display = ('label', 'is_active', 'uploaded_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
