from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from django.db.models import Q

from .models import Profile, Message
from .forms import CustomUserCreationForm , ProfileForm , SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser (request):
    page = 'login'
    
    # If someone is already logged in, they can't see the login page again (Corner Case lol)
    if request.user.is_authenticated:   
        return redirect('profiles')
        
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:    # Check if this 'user' exists in the database
            user = User.objects.get(username=username)
        except: # If no, print that it doesn't exist
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)
            # 'authenticate' function matches the pw w/ the username in the DB
        
        if user is not None:    # i.e., user != NULL
            login(request, user)    # This keeps the user logged in, while on the site
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')
        
    return render(request, 'users/login_register.html')

def logoutUser (request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')

def registerUser (request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User Account was Created')
            
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occured during registration')
    
    context = {'page':page, 'form':form}
    return render(request, "users/login_register.html", context)

def profiles (request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, results=6)
    
    context = {'profiles':profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, "users/profiles.html", context)

def userProfile (request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
        # Exclude every single skill whose description matches ("") (i.e., empty string). So, it'll
        # only include the skills that have a description
    otherSkills = profile.skill_set.filter(description="")
        # This only filters the skills that have no description (empty string)
    
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@ login_required(login_url='login')
def userAccount (request):
    profile = request.user.profile      # One-to-One Relationship
    
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@ login_required(login_url='login')
def editAccount (request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)    # Pre-fill the fields w/ the existing user information
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect('account')
        
    context = {'form':form}
    return render(request,'users/profile_form.html', context)

@ login_required(login_url='login')
def createSkill (request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            
            skill.save()
            messages.success(request, 'Skill was added Successfully!!')
            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@ login_required(login_url='login')
def updateSkill (request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        
        if form.is_valid():
            form.save()    
            messages.success(request, 'Skill was updated Successfully!!')
            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

@ login_required(login_url='login')
def deleteSkill (request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted!!')
        return redirect('account')
    
    context = {'object':skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    
    unreadCount = messageRequests.filter(is_read=False).count()
    
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    
    if message.is_read == False:    # If this message was 'unread', and being opened for the first time, change its status to 'read', and save the update
        message.is_read = True
        message.save()
        
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm
    
    try:
        sender = request.user.profile
    except:
        sender = None
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            
            message.sender = sender
            message.recipient = recipient
            
            if sender:  # If sender is already logged in, we won't ask for his/her name and email id. Instead, we'll fill them up in the backend, using his account info
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            messages.success(request, 'Your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)
    
    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html', context)