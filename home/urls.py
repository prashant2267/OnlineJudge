from django.contrib import admin
from django.urls import path, include
from home import views
urlpatterns = [
    path('',views.index, name="home"),
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser, name="logout"),
    path('problems',views.allproblems, name="problems"),
    path('problem/<int:problem_id>/', views.problemDetail, name="problem_detail"),
    path('problem/<int:problem_id>/submit/', views.submitProblem, name="submit"),
    path('leaderboard/',views.leaderboard, name="leaderboard"),
    
]

