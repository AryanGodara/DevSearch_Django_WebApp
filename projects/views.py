from django.core import paginator
from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

# Create your views here.


"""Both the functions below, return type is HttpResponse class, which has an 'editable' string
as the content. They have 1 and 2 parameters, respectively"""

def projects (request) :
    projects, search_query = searchProjects(request)
    
    custom_range, projects = paginateProjects(request, projects, results=6)
        
    context = { 'projects' : projects, 'search_query':search_query, 'custom_range':custom_range}
    # The key and value name can be different from each other, we use the key to access the value
    
    return render(request , 'projects/projects.html' , context)


"""This pk (primary/key) is written in the address of the webpage, like ''/project/pk"""
def project (request , pk ) :
    # projectObj = None       # Kinda like NULL
    
    """Don't need the three lines below anymore, not deleting due to possibility for revision"""
    # for i in projectstList :
    #     if i['id'] == pk:   # We found a match, basic for(){ if(){do_this} else(){continue} }
    #         projectObj = i ;    #Here, i is of type 'dictionary'
    
    """Instead of just quering the 'tags' right here, we can instead, access them from the templates"""
    # projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()    # This gives us all the tags for this object
    # return render(request , 'projects/single-project.html' , {'project':projectObj , 'tags':tags})
    
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm (request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount     # Update the vote count for this project in the databse
        
        messages.success(request, 'Your review was successfully Submitted!')
        
        return redirect('project', pk=projectObj.id)
    
    return render(request , 'projects/single-project.html' , {'project':projectObj , 'form' : form})
    

# Used a 'decorator': prevents logged-out/random users from creating a new project
@ login_required(login_url='login')     # They'll be redirected to the login page
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        
        #print(request.POST)            # These two lines are just plyaing around with the submit button
        #print(request.POST['title']) # Like using mp[key] in C++
        form = ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():  # Django makes sure that all the things about the form are valid
            project = form.save(commit=False)
            project.owner = profile     # Attach the newly created project to the 'cur' profile
            
            project.save()
            
            return redirect('account') # Then, redirect them to the projects.html page
    
    context = {'form':form}
    return render(request,"projects/project_form.html",context)


"""Fourth function : Updating a Project"""
@ login_required(login_url='login')     # They'll be redirected to the login page
def updateProject (request,pk):
    profile = request.user.profile
    project = Project.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=project)
        
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form':form}
    return render(request,"projects/project_form.html",context)



"""Fourth Function : Deleting a Project"""
@ login_required(login_url='login')     # They'll be redirected to the login page
def deleteProject (request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects') # Send them back to the 'projects' page
    
    context = {'object':project}
    return render(request,"delete_template.html",context)