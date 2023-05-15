from django.contrib import admin
from .models import News, Comment, NewsReaction, Photo, CommentPhoto, Trainer, Schedule


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'news', 'content', 'date')
    list_filter = ('date',)


class NewsReactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'news', 'reaction_type', 'date')
    list_filter = ('reaction_type', 'date')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'content', 'photo')
    list_display_links = ('title', 'content', 'photo')
    list_filter = ('publication_date',)
    prepopulated_fields = {'slug': ('title',)}


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'photo', 'publication_date')
    prepopulated_fields = {'slug': ('title',)}


class CommentPhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'author', 'content', 'date')
    list_filter = ('photo', 'author')
    search_fields = ('photo__title', 'author')


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'photo', 'contact_phone', 'information')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'weekday', 'forma', 'group', 'trainer')


admin.site.register(Comment, CommentAdmin)
admin.site.register(NewsReaction, NewsReactionAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(CommentPhoto, CommentPhotoAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
