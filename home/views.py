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
from datetime import datetime


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
    user_submission_file = rf'C:\Django\onlinejudge\home\uploads\usersubmissions\{problem_id}_{request.user.id}_{datetime.now()}.cpp' #1_xyz_2021-06-25 07:58:56.550604
    with open(user_submission_file, 'wb+') as dest:
         for chunk in f.chunks():
             dest.write(chunk)
    os.system(f'g++ {user_submission_file}.cpp -o {user_submission_file}.out')
    # t1 = Testcases.objects.filter(probl); // t1 is the test case of problem_id
    testcase_input_file = t1.input; 
    testcase_output_file = t1.output; 

    os.system(rf'{user_submission_file}.out < {testcase_input_file} > C:\Django\onlinejudge\home\out.txt')
    
    out1= r'C:\Django\onlinejudge\home\out.txt'
    out2= testcase_output_file
    if (filecmp.cmp(out1, out2, shallow=False)):
         verdict = 'Accepted'           
    else:
         verdict = 'Wrong Answer'  
    
    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = user_submission_file
    solution.save()
    
    return HttpResponseRedirect(reverse('home:leaderboard'))

def leaderboard(request):
    solutions = Solution.objects.all()
    return render(request, 'home/leaderboard.html', {'solutions': solutions}) 
