project_home="/Users/jackmoxon/measurr/measurr/pg/"

import sys, os
sys.path.append(project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'measurr.settings'

from pg.models import *

one = {"question":"Is it tied to revenue?",
       "c1":"Very much so.",
       "c1v":100,
       "c2": "A bit.",
       "c2v":50,
       "c3": "Not a 'tall.",
       "c3v":10, 
}

two = {"question":"Is it really hard?",
       "c1":"There are only a handful of people that can do this",
       "c1v":100,
       "c2": "Many in the org can do this",
       "c2v":50,
       "c3": "Anyone in the organization can do this.",
       "c3v":10,
}

three = {"question":"Are other tasks blocked by this?",
       "c1":"Many",
       "c1v":100,
       "c2": "A few",
       "c2v":50,
       "c3": "None",
       "c3v":10,
}

four = {"question":"How long might it take",
       "c1":"Months",
       "c1v":100,
       "c2": "Weeks.",
       "c2v":50,
       "c3": "Days.",
       "c3v":10,
}

data = (one, two, three, four)

for i in data:
    question = PriorityQuestion()
    question.question = i['question']
    question.save()
    question.prioritychoice_set.create(choice_text=i['c1'], choice_value=i['c1v'])
    question.prioritychoice_set.create(choice_text=i['c2'], choice_value=i['c2v'])
    question.prioritychoice_set.create(choice_text=i['c3'], choice_value=i['c3v'])
    question.save()
    

