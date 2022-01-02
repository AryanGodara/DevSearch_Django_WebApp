"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path , include # Now we've imported both path and include functions
from django.http import HttpResponse

from django.conf import settings    # Have access to the settings.py file
from django.conf.urls.static import static  #This will help us create URLs for our static files

from django.contrib.auth import views as auth_views     # We're going to use 'auth_views.view_name' instead of simply using, 'views.view_name'


"""
This is currently a small program, but when we work on a very large scale, things will start
to get really messy. So, instead of just defining all the functions here in 'urls.py', we 
should instead, we should separate these. So we're going to let our projects app take care of 
any view and your URLs that deals with projects
"""
#! And so, I've commented out all the code here, and we'll write in this the separate
#! 'projects app' to keep things organized
"""
# Create a function for returning back some projects
def projects (request): # request object is the parameter, 'projects' is the function name
    return HttpResponse('Here are our projects')
# http://127.0.0.1:8000/projects/           'this opens the above page'


def project (request,pk): #Now, we need to enter two parameters to open this page
    return HttpResponse("Single Project : " + str(pk) )
# http://127.0.0.1:8000/projects/           'this  DOESN'T open the above page'
# We need to have two parameters, so instead, we write
# http://127.0.0.1:8000/project/1/           'this opens the above page'
# OR http://127.0.0.1:8000/project/2/       'This 1 or 2 is the 'string' value stored in pk
# We can similarly add multiple parameters to each function

path('projects/',projects,name="projects"),
path('project/<str:pk>/',project,name="project"),   # string value : pk (primary key)

We can also no longer, use the above two lines,  since we've shifted these functions to views.py
of the projects folder, or projects app. Which stores everything related to the projects 
section of our website
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(''),   # The empty string means the root domain; admin/ means rootdomain/admin/
    path('projects/',include('projects.urls')),  #go to projects.urls, and import everything
    path('',include('users.urls')),  #go to users.urls, and import everything
    
    #! Path for the API stuff starts
    path('api/', include('api.urls')),  #* Similar to what we did above for 'users.urls'
    #! Path for the API stuff ends
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]

# Appending to the urlpatterns list, instead of adding everything to the same list above
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Appending to the urlpatterns list, instead of adding everything to the same list above
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#* The 4 views written below, are built-in views, in Django. And they come with a lot of usefult functionality
#* which is more than enough to set up the 'forgot password' views for our project.
#? 1 - User submits email for reset                 // PasswordResetView.as_viwe()              // name="reset_password"
#? 2 - Email sent message                           // PasswordResetDoneView.as_view()          // name="password_reset_done"
#? 3 - Email with link and reset instructions       // PasswordResetConfirmView.as_view()       // name="password_reset_confirm"
#? 4 - Password successfully reset message          // PasswordResetCompleteView.as_view()      // name="password_reset_complete"
