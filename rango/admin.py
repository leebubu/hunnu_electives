from django.contrib import admin

# Register your models here.
from rango.models import Category, Subject, Answers, Campus, AnswerUserLikes, AnswerUserDislikes
from rango.models import UserProfile

class CampusAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
	list_display = ('name', 'name_ch')

class SubjectAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('title', 'title_ch', 'campus')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'name_ch', 'subject')
	
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'author', 'content', 'category')
	
class AnswerUserLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'answer')

class AnswerUserDislikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'answer')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(Answers, AnswersAdmin)
admin.site.register(Campus, CampusAdmin)
