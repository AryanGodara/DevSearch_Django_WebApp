from django.urls import path
from . import views # '.' means, import from the current package, and we imported all things
                    # from the 'views.py' file

urlpatterns = [
    path('' , views.projects , name = "projects"), # add views. to the file path
    path('project/<str:pk>/' , views.project , name = "project"),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
]