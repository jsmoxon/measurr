from django.contrib import admin
from pg.models import *

admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskRating)
admin.site.register(TaskHowWell)
admin.site.register(Manager)


class ChoiceInline(admin.TabularInline):
    model = PriorityChoice
    extra = 3

class PriorityQuestionAdmin(admin.ModelAdmin):
    inlines= [ChoiceInline]


admin.site.register(PriorityQuestion, PriorityQuestionAdmin)


