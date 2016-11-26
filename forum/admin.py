from django.contrib import admin
from forum.models import Category, Question, Answer


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'inviting_person')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
