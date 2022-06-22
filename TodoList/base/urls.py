from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,UpdateTask,TaskDelate,CustomLogin,registrazione
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',CustomLogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',registrazione.as_view(), name='registerpage'),

    path('',TaskList.as_view(),name='taskspage'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='tasksDetail'),
    path('task-create/',TaskCreate.as_view(),name='taskcreate'),
    path('task-edit/<int:pk>/',UpdateTask.as_view(),name='taskupdate'),
    path('task-delate/<int:pk>/',TaskDelate.as_view(),name='taskdelate'),
]
