from models import *
from django.forms import ModelForm, Textarea, HiddenInput
from django import forms


class TaskEntryForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'primary_assignee', 'priority_rank')
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5}),
            'priority_rank': HiddenInput(),
        }

class TaskEntryFormChoice(forms.Form):
    choice_list = forms.CharField(widget=forms.HiddenInput)

class TaskRatingForm(ModelForm):
#    is_task_complete = forms.BooleanField()
    class Meta:
        model = TaskRating
        fields = ('how_well','long_review', 'how_quickly')
        labels = {
            'how_well':'How Well Was it Done?',
            'long_review':'Please review in detail here:',
            }
        widgets = {
            'long_review': Textarea(attrs={'cols': 40, 'rows': 10}),
        }

class CreateUserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','password', 'email')
        widgets = {
            'password' : forms.PasswordInput()
        }

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'due_date', 'description', 'questions', 'workers',)
        widgets = {
            'workers': forms.CheckboxSelectMultiple(),
            'questions': forms.CheckboxSelectMultiple(),
            'description': Textarea(attrs={'cols':120, 'rows': 10}),
            
            }
        labels = {
            'name':'Project Name',
            'description':'Project Description',          
            'questions': 'What questions do you want to use to evaluate each task?',
            'workers':'Who do you want to assign to this project?',
            }

class AddWorkerToProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('workers',)


#unclear if this is being used
class TaskRankingForm(ModelForm):
    class Meta:
        model = PriorityQuestion
        


                       
             


