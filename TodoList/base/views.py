from asyncio import tasks
from msilib.schema import Class
from multiprocessing import context
from urllib import request
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.



class CustomLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('taskspage')

class registrazione(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('taskspage')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(registrazione, self).form_valid(form)
        
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskspage')
        return super(registrazione, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        ricerca_input = self.request.GET.get('area-ricerca') or ''
        if ricerca_input:
            context['tasks'] = context['tasks'].filter(title_startswith = ricerca_input)
        context['ricerca_input'] = ricerca_input
        return context
        


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','descrizione','completato']
    success_url = reverse_lazy('taskspage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','descrizione','completato']
    success_url = reverse_lazy('taskspage')

class TaskDelate(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('taskspage')
    template_name = 'base/task_confirm_delate.html'