from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup),
    path('add-task/', views.add_task),
    path('logout/', views.signout),
    path('delete-task/<str:id>', views.delete_task),
    path('change-status/<str:id>/<str:status>', views.change_task),
]