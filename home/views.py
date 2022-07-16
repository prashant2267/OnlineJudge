import imp
from time import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
import os, filecmp

from home.models import Problem, Solution
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(username=username, password=password)
      if user is not  None:
       login(request, user)   
       return redirect("/")
      else:    
           return render(request, 'login.html')
       
    return render(request, 'login.html') 
def logoutUser(request):
    logout(request)
    return redirect("/login")

def allproblems(request):
   problems_list = Problem.objects.all()
   context = {'problems_list': problems_list}
   return render(request, 'index1.html', context)

def problemDetail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, 'detail.html', {'problem': problem})

def submitProblem(request, problem_id):
    f = request.FILES['solution']
    with open('/Users/suranamudit/solution.cpp', 'wb+') as dest:
         for chunk in f.chunks():
             dest.write(chunk)
    os.system('g++ /Users/suranamudit/solution.cpp')
    os.system('./a.out < /Users/suranamudit/inp.txt > /Users/suranamudit/out.txt')
    
    out1= '/Users/suranamudit/out.txt'
    out2= '/Users/suranamudit/actual_out.txt'
    if (filecmp.cmp(out1, out2, shallow=False)):
         verdict = 'Accepted'           

    else:
         verdict = 'Wrong Answer'  
    
    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = '/Users/suranamudit/solution.cpp'
    solution.save()
    
    return HttpResponseRedirect(reverse('home:leaderboard'))

def leaderboard(request):
    solutions = Solution.objects.all()
    return render(request, 'home/leaderboard.html', {'solutions': solutions}) 
