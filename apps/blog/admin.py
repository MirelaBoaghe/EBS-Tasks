from django.contrib import admin

from apps.blog.models import Blog, Category, Comments

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "enabled"]

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(Comments, CommentAdmin)