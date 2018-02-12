import timedate

from django.shortcuts import render
from django.http import HttpResponse

from education.models import User, Question

from django.utils import timezone

# Create your views here.
def index(request):
	return HttpResponse("Hello, fellow team members, you're at the education index.")

#associate the new question to the appropriate user
def add_question(request, new_title, new_programming_language, new_level, new_description, new_solution, new_user):
	q = Question(title=new_title, programming_language=new_programming_language, level=new_level, description=new_description, solution=new_solution, pub_date=timezone.now(), user=User.objects.get(temp_usr=new_user))
	q.save()
	user.question_set.add(q)
	msg = "New question added to %s" % (new_user)
	return HttpResponse(msg)