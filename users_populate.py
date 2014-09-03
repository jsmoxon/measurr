project_home="/Users/jackmoxon/measurr/measurr/pg/"

import sys, os
sys.path.append(project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'measurr.settings'

from pg.models import *

one = {'username':'scrooge',
       'pass':'pw',
       'email':'escrooge@j.com'}
two = {'username':'cratchet',
       'pass':'pw',
       'email':'bcratchet@j.com'}

def create_users():
    data = (one, two)
    for i in data:
        user = User()
        user.username = i['username']
        user.pw = i['pass']
        user.email = i['email']
        user.save()
    
def create_manager():
    manager=Manager()
    user = UserProfile.objects.get(pk=1)
    print user
    manager.user_profile = user
    manager.save()
    manager.is_manager = True
    manager.save()

def create_profiles():
    users = User.objects.all()
    for user in users:
        profile = UserProfile()
        profile.user = user
        profile.save()
        print profile

import datetime
def create_project():
    project = Project()
    project.manager = Manager.objects.get(pk=1)
    project.name = "Jack's first project"
    project.description = "Jack's first project description"
    project.notes = "Notes for Jack's first project"
    project.due_date = datetime.datetime.now()
    project.save()

#functions that get called
create_users()
create_profiles()
create_manager()
create_project()
