from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    #raw crit score of all completed tasks
    raw_crit_score = models.IntegerField(blank=True, null=True, default=0)
    #raw crit divided by tasks completed
    avg_crit_score = models.IntegerField(blank=True, null=True, default=0)
    raw_how_well_score = models.FloatField(blank=True, null=True, default=0)
    avg_how_well_score = models.FloatField(blank=True, null=True, default=0)
    #not using today because it's now an org thing: 
    department = models.CharField(max_length=100, blank=True, null=True)

    def comp_tasks_number(self):
        return len(Task.objects.filter(primary_assignee=self, is_completed=True))
    
    def get_completed_tasks(self):
        return Task.objects.filter(primary_assignee=self, is_completed=True)
        
    def update_well_scores(self):
        completed_tasks = Task.objects.filter(primary_assignee=self, is_completed=True)
        task_ratings = []
        list_of_scores = []
        for task in completed_tasks:
            for rating in task.task_rating.all():
                task_ratings.append(rating.how_well.score)
        self.raw_how_well_score = sum(task_ratings)
        self.save()
        self.avg_how_well_score = self.raw_how_well_score/len(completed_tasks)
        return self.save()

    def segment_how_well_scores(self):
        excellent = 0
        good = 0
        poor = 0
        for task in self.get_completed_tasks():
            for rating in task.task_rating.all():
                if rating.how_well.name == "Poor":
                    poor +=1
                elif rating.how_well.name == "Good":
                    good +=1
                elif rating.how_well.name == "Excellent":
                    excellent +=1
        return {'excellent':excellent, 'good':good, 'poor':poor}

    def segment_task_difficulty(self):
        hard = 0
        moderate = 0
        easy = 0
        for task in self.get_completed_tasks():
            for choice in task.priority_choices.filter(key="difficulty"):
                if choice.choice_value == 100:
                    hard +=1
                elif choice.choice_value == 50:
                    moderate +=1
                elif choice.choice_value == 10:
                    easy +=1
        return {'hard':hard, 'moderate':moderate, 'easy':easy}

    def segment_how_quickly(self):
        early = 0
        ontime = 0
        late = 0
        for task in self.get_completed_tasks():
            for rating in task.task_rating.all():
                #should go off key rather than score ultimately
                if rating.how_quickly is not None and rating.how_quickly.score == 100:
                    early +=1
                elif rating.how_quickly is not None and rating.how_quickly.score == 75:
                    ontime+=1
                elif rating.how_quickly is not None and rating.how_quickly.score == 10:
                    late+=1
        return {'early':early, 'ontime':ontime, 'late':late}

    def update_raw_crit_score(self):
        completed_tasks = Task.objects.filter(primary_assignee=self, is_completed=True)
        list_of_scores = []
        for task in completed_tasks:
            list_of_scores.append(task.priority_rank)
        sum_scores = sum(list_of_scores)
        self.raw_crit_score = sum_scores
        return self.save()
        
    def update_avg_crit_score(self):
        completed_tasks_number = len(Task.objects.filter(primary_assignee=self, is_completed=True))
        self.avg_crit_score = self.raw_crit_score//completed_tasks_number
        return self.save()        
    
    def segment_task_criticality(self):
        completed_tasks = Task.objects.filter(primary_assignee=self, is_completed=True)
        high = 0
        med = 0
        low = 0
        for task in completed_tasks:
            if task.priority_rank < 150: 
                low +=1
            elif task.priority_rank < 300:
                med +=1
            elif task.priority_rank >300:
                high +=1
            else:
                print "none avail" 
        return {'high':high, 'med':med, 'low':low} 
    
    def __unicode__(self):
        return str(self.user)

class Organization(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    user_profile = models.ManyToManyField(UserProfile)
    def __unicode__(self):
        return str(self.name)

class Manager(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    is_manager = models.NullBooleanField()
    def __unicode__(self):
        return str(self.user_profile)    
    
class PriorityQuestion(models.Model):
    question = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.NullBooleanField()
    def __unicode__(self):
        return self.question

class PriorityChoice(models.Model):
    priority_question = models.ForeignKey(PriorityQuestion)
    choice_text = models.CharField(max_length=1000, blank=True, null=True)
    choice_value = models.IntegerField()
    key = models.CharField(max_length=1000, blank=True, null=True)
    def __unicode__(self):
        return self.choice_text

class Project(models.Model):
    manager = models.ForeignKey(Manager)
    workers = models.ManyToManyField(UserProfile)
    questions = models.ManyToManyField(PriorityQuestion)
    name = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def create_intro_task(self):
        task = Task(name="Create more tasks for this project", project=self, 
                    description="Use the Create Task button to add more tasks and assign people to them.", 
                    primary_assignee=self.workers.all()[0], priority_rank=500)
        return task.save()

    def __unicode__(self):
        return self.name

class TaskHowWell(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    def __unicode__(self):
        return self.name

class TaskHowQuickly(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    key = models.CharField(max_length=100, blank=True, null=True, unique=True)
    def __unicode__(self):
        return self.name

class TaskRating(models.Model):
    reviewer = models.ForeignKey(UserProfile, null=True, blank=True)
    future_review_date = models.DateField(null=True, blank=True)
    long_review = models.TextField(blank=True, null=True)
    how_well = models.ForeignKey(TaskHowWell, null=True, blank=True)
    how_quickly = models.ForeignKey(TaskHowQuickly, null=True, blank=True)
    def __unicode__(self):
        return str(self.reviewer)

class Task(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True, null=True)
    primary_assignee = models.ForeignKey(UserProfile)
    priority_rank = models.IntegerField(blank=True, null=True)
    future_eval_interval = models.IntegerField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_reviewed_by_manager = models.NullBooleanField(default=False)
    task_rating = models.ManyToManyField(TaskRating, blank=True, null=False)
    priority_choices = models.ManyToManyField(PriorityChoice, null=True, blank=True)

    def __unicode__(self):
        return self.name


