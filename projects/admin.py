from django.contrib import admin

# Register your models here.

from .models import Project , Review , Tag
# import the classes 'Project' , 'Review' , 'Tag' from the file 'models.py' which is also in this directory

admin.site.register(Project)    # Get this model and show it in the admin panel
admin.site.register(Review)    # Get this model and show it in the admin panel
admin.site.register(Tag)    # Get this model and show it in the admin panel
