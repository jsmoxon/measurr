from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import *
from forms import *

def main_dashboard(request):
    user_profile = request.user.get_profile()
    projects = Project.objects.filter(workers=user_profile)
    cleaned_worker_list = Organization.objects.get(user_profile=user_profile).user_profile.all()
    return render(request, 'main_dashboard.html', {'projects':projects, 
                                                   'user_profile':user_profile,
                                                   'cleaned_worker_list':cleaned_worker_list})

def create_new_project(request):
    user_profile = request.user.get_profile()
    organization = Organization.objects.get(user_profile=user_profile)
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            manager = Manager.objects.get_or_create(user_profile=user_profile)
            project = Project.objects.create(name=form.cleaned_data['name'],
                                             due_date=form.cleaned_data['due_date'],
                                             description=form.cleaned_data['description'],
                                             manager=manager[0])
            project.save()
            for question in form.cleaned_data['questions']:
                project.questions.add(question)
            for worker in form.cleaned_data['workers']:
                project.workers.add(worker)
            project.workers.add(user_profile)
            project.create_intro_task()
            return redirect('main_dashboard')
        else:
            return HttpResponse("fail")
    else:
        form = CreateProjectForm()
        form.fields["workers"].queryset = Organization.objects.get(user_profile=user_profile).user_profile.all()

    return render(request, 'create_new_project.html', {'form':form})



def newuser(request):
    """creates a new user and attached them to an organization; probably still needs to do an email validation etc."""
    user_profile = request.user.get_profile()
    organization = Organization.objects.get(user_profile=user_profile)
    if request.method == 'POST':
        form = CreateUserProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['username'],form.cleaned_data['password'])
            user.save()
            profile = UserProfile.objects.create(user=user)
            profile.save()
            organization.user_profile.add(profile)
            return redirect('main_dashboard')
        else:
            return HttpResponse("fail")
    else:
        form = CreateUserProfileForm()
    return render(request, 'newuser.html', {'form':form})

def project_page(request, project_id):
    user_profile = request.user.get_profile()
    project = Project.objects.get(pk=project_id)
    pending_tasks = Task.objects.filter(project=project_id, is_completed=False).order_by('-priority_rank')
    completed_tasks =Task.objects.filter(project=project_id, is_completed=True).order_by('-priority_rank')
    completion_percentage = 100*(float(len(completed_tasks))/(float(len(completed_tasks))+float(len(pending_tasks))))
    #float(len(completed_tasks)/(len(pending_tasks)+len(completed_tasks)))
    workers = project.workers.all()
    context = {'user_profile':user_profile, 'project': project, 'pending_tasks':pending_tasks, 
               'completed_tasks':completed_tasks, 'workers':workers, 'completion_percentage': completion_percentage}
    return render(request, 'projects_page.html',context)

def add_user_to_project(request, project_id):
    user_profile = request.user.get_profile()    
    org_worker_list = Organization.objects.get(user_profile=user_profile).user_profile.all()
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = AddWorkerToProjectForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['workers']
            for worker in form.cleaned_data['workers']:
                project.workers.add(worker)
            return redirect('project_page', project_id)

        else:
            return HttpResponse("fail")
    else:
        form = AddWorkerToProjectForm()
        form.fields["workers"].queryset = Organization.objects.get(user_profile=user_profile).user_profile.all()
    return render(request, 'add_user_to_project.html', {'form':form, 'project':project})

def create_task(request, project_id):
    user_profile = request.user.get_profile()
    project = Project.objects.get(pk=project_id)
    questions = project.questions.all()
    if request.method == 'POST':
        form = TaskEntryForm(request.POST)
        choice_form = TaskEntryFormChoice(request.POST)
        if form.is_valid():
            task = Task()
            task.name = form.cleaned_data['name']
            task.project = project
            task.description = form.cleaned_data['description']
            task.primary_assignee = form.cleaned_data['primary_assignee']
            task.save()
            print choice_form
            choices = []
            choice_list = str(choice_form.cleaned_data['choice_list'])
            for i in choice_list.split(','):
                choices.append(int(i))
            priority_rank = 0
            for choice in choices:
                selected_choice = PriorityChoice.objects.get(pk=choice)
                task.priority_choices.add(selected_choice)
                priority_rank += selected_choice.choice_value
            task.priority_rank = priority_rank
            task.save()
            return redirect('project_page', project_id)
        else:
            return HttpResponse("Couldn't upload task. Please contact support.")
    else:
        form = TaskEntryForm()
        choice_form = TaskEntryFormChoice()
        form.fields["primary_assignee"].queryset = Organization.objects.get(user_profile=user_profile).user_profile.all()
        
    return render(request, 'task_entry_form.html', {'form':form, 'questions':questions, 'project':project, 'choice_form':choice_form})
        
def view_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task_project_id = task.project.id
    return render(request, 'task_view.html', {'task':task})


def review_task(request, task_id):
    """lets you look at the task info and submit it as complete and review it; still needs significant work - multiple reviews from different folks etc. """
    user_profile = request.user.get_profile()
    task = Task.objects.get(pk=task_id)
    task_project_id = task.project.id
    if request.method == 'POST':
        rating_form = TaskRatingForm(request.POST)
        if rating_form.is_valid():
            task_rating = TaskRating()
            task_rating.long_review = rating_form.cleaned_data['long_review']
            task_rating.how_well = rating_form.cleaned_data['how_well']
            task_rating.how_quickly =rating_form.cleaned_data['how_quickly']
            task_rating.reviewer = user_profile
            task_rating.save()
            task = Task.objects.get(pk=task_id)
            task.is_completed = True
            task.task_rating.add(task_rating.id)
            task.save()
            task.primary_assignee.update_raw_crit_score()
            task.primary_assignee.update_avg_crit_score()
            task.primary_assignee.update_well_scores()
            if task.project.manager.user_profile == user_profile:
                task.is_reviewed_by_manager = True
                task.save()

            return redirect('project_page',task_project_id)
        else:
            return HttpResponse("fail")
    else:
        form = TaskEntryForm()
        rating_form = TaskRatingForm()
    return render(request, 'task_review.html', {'form':form, 'task':task, 'rating_form':rating_form})


def employee_dashboard(request, employee_id):
    """the dashboard that is seen by managers when looking at employees; employees can see only see their own, permissions not set up yet but soon"""
    user_profile = request.user.get_profile()
    projects = Project.objects.filter(workers=employee_id)
    employee = UserProfile.objects.get(pk=employee_id)
    pending_tasks = Task.objects.filter(primary_assignee=employee_id, is_completed=False).order_by('-priority_rank')
    completed_tasks =Task.objects.filter(primary_assignee=employee_id, is_completed=True).order_by('-priority_rank')
    completed_tasks_number = len(completed_tasks)
    criticality_pie_data = employee.segment_task_criticality()
    how_well_pie_data =  employee.segment_how_well_scores()
    difficulty_pie_data = employee.segment_task_difficulty()
    how_quickly_bar_data = employee.segment_how_quickly()
    context = {'user_profile':user_profile, 'pending_tasks':pending_tasks,
               'completed_tasks':completed_tasks, 'employee':employee, 
               'completed_tasks_number':completed_tasks_number, 
               'how_well_pie_data':how_well_pie_data, 'criticality_pie_data':criticality_pie_data,
               'difficulty_pie_data':difficulty_pie_data, 'how_quickly_bar_data':how_quickly_bar_data}
 
    return render(request, 'employee_dashboard.html', context)


def manager_dashboard(request):
    return

