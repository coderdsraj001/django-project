from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Category, Tag, Comment, User
from django.utils.html import format_html
from import_export.admin import ExportActionMixin

# Register your models here.
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'desc']
    list_filter = ['name']
    search_fields = ['name']

class TagsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'desc']
    list_filter = ['name']
    search_fields = ['name']

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment_content', 'post_title',]
    list_filter = ['name']
    search_fields = ['name']

    def post_title(self, obj):
        return format_html(f"<p>{obj.post}</p>")

    def user_name(self, obj):
        return format_html(f"<p>{obj.user.first_name}</p>")

class PostModelAdmin(admin.ModelAdmin):
    def post_title(self, obj):
        return format_html(f"<a href='/post/{obj.slug}'>{obj.title}</a>")

    def post_image(self, obj):
        if obj.feature_img:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.feature_img.url))
        else:
            return ''
    fields = ['author', 'thumbnail_img',  'feature_img', 'title', 'text', 'category', 'tags', 'created_date',]
    list_filter = ['author', 'title', 'category', 'tags', 'published_date']
    list_display = ['author', 'post_image', 'post_title', 'category', 'published_date']
    search_fields = ['title', 'category', 'tags']
    view_on_site = True

class UserModelAdmin(ExportActionMixin, admin.ModelAdmin):
    def profile(self, obj):
        if obj.user_img:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.user_img.url))
        else:
            return ''
    list_display = ['first_name', 'username', 'user_img', 'email', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country']
    list_filter = ['first_name',  'email','user_img', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country']
    search_fields = ['first_name',  'email','user_img', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country']


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Tag, TagsModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(User, UserModelAdmin)
