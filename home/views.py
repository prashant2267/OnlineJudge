import subprocess
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


from home.models import Problem, Solution, Testcases
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
    # use relative path
    # absolute path vs relative path
    user_file_prefix = rf'C:\Django\onlinejudge\home\uploads\usersubmissions\{problem_id}_{request.user.id}_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}' #1_xyz_2021-06-25 07:58:56.550604
    
    user_code_file = f"{user_file_prefix}.cpp"
    user_executable_file = f"{user_file_prefix}.exe"
    
    #Copies code of user into this file
    with open(user_code_file, 'wb+') as dest:
         for chunk in f.chunks():
             dest.write(chunk)


    # Code which is syntactically wrong, will throw an error. you can use try and catch . 
    os.system(f'g++ {user_code_file} -o {user_executable_file}') #Use subprocess module instead of os
   
    test_cases = Testcases.objects.filter(problem=problem_id);  # [TestCase1, TestCase2...]
   
    flag = True; 
   
    for testcase in test_cases: 
        testcase_input_file = testcase.input; 
        testcase_output_file = testcase.output; 


        #use relative path. 
        out1= r'C:\Django\onlinejudge\home\out.txt'


        output = subprocess.check_output(user_executable_file, stdin=open(testcase_input_file)).decode("utf-8")
        
        with open(out1, "w") as dest: 
            dest.write(output)

        if not(filecmp.cmp(out1, testcase_output_file, shallow=False)): 
            flag = False; 
            break 

    if flag:
         verdict = 'Accepted'           
    else:
         verdict = 'Wrong Answer'  
    
    solution = Solution()
    solution.problem = Problem.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = user_code_file
    solution.save()
    
    return redirect('leaderboard')

def leaderboard(request):
    solutions = Solution.objects.all()
    return render(request, 'leaderboard.html', {'solutions': solutions}) 
