from django.shortcuts import render , redirect
from base.models import*
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView , FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login






# Create your views here.



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')








class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm

    success_url = reverse_lazy('tasks') 
    
    def form_valid(self, form):
        user  = form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterPage , self).form_valid(form)
    
    def get(self , *args , **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage , self).get(*args , **kwargs)
    







class TaskList(LoginRequiredMixin  , ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/taskList.html'
    
    
    #this method is present in listview we are overriding oot to return the list of the logged in user 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)  
        context['count'] = context["tasks"].filter(complete = False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)
        
        #this will put the valu
        context['search_input'] = search_input
        
        
        return context

        
        
        

    



class TaskDetail(LoginRequiredMixin , DetailView):
    model = Task
    context_object_name = 'task' #this basically tells the name with which our object will be available in the template
    template_name = 'base/task.html'



    
class TaskCreate (LoginRequiredMixin  , CreateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')   #that is whenever we create an item or task we want to be redirected to the tasks page
    
    def form_valid(self , form):
        form.instance.user = self.request.user
        return super(TaskCreate , self).form_valid(form)
    
    
    
class TaskUpdate(LoginRequiredMixin ,UpdateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')   #that is whenever we create an item or task we want to be redirected to the tasks page
        



class DeleteView(LoginRequiredMixin  , DeleteView):
    model = Task
    context_object_name = 'task'
    success_url  = reverse_lazy('tasks')
    



















