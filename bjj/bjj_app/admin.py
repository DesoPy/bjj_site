from django.contrib import admin
from .models import News, Comment, NewsReaction


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'news', 'date')
    list_filter = ('date',)


class NewsReactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'news', 'reaction_type', 'date')
    list_filter = ('reaction_type', 'date')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'content', 'photo')
    list_display_links = ('title', 'content', 'photo')
    list_filter = ('publication_date',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment, CommentAdmin)
admin.site.register(NewsReaction, NewsReactionAdmin)
admin.site.register(News, NewsAdmin)
