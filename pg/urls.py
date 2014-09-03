from django.conf.urls import patterns, url

from pg import views

urlpatterns = patterns('',
    url(r'^$', views.main_dashboard, name='main_dashboard'),
    url(r'^newuser/$', views.newuser, name='newuser'),                       
    url(r'^create_new_project/$', views.create_new_project, name='create_new_project'),
    url(r'^project/(?P<project_id>\d+)/$', views.project_page, name='project_page'),
    url(r'^project/(?P<project_id>\d+)/add_user/$', views.add_user_to_project, name='add_user'),
    url(r'^project/(?P<project_id>\d+)/create_task/$', views.create_task, name='create_task'),
    url(r'^task/(?P<task_id>\d+)/$', views.view_task, name='view_task'),
                       
#need to change the url to be more interesting here for employee page
    url(r'^employee/(?P<employee_id>\d+)/$', views.employee_dashboard, name='employee_dashboard'),

                           
)
