from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Choice

# <HINT> Register QuestionInline and ChoiceInline classes here

class LessonInLine(admin.StackedInline):
    model = Lesson
    extra = 5

class QuestionInLine(admin.StackedInline):
    model = Question

class ChoiceInLine(admin.StackedInline):
    model = Choice

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInLine]
    list_display = ('name', 'pub_date') # what fields to display
    list_filter = ['pub_date'] # you can filter by date
    search_fields = ['name', 'description'] # you can search by name and desc

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInLine, ChoiceInLine] # adds Lesson to Course admin
    list_display = ['title']

# <HINT> Register Question and Choice models here

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question)
admin.site.register(Choice)


