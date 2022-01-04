# We're going to use a lot of model forms down the road, and this is where they'll be stored

from django import forms
from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        #fields = '__all__'
        # When we use '__all__', instead of writing a list ( ['a','b','c',...] ), we just tell django to
        # create a form that contains all the 'editable' fields from the 'model', which is the 'Project'
        # class defined in view.py. These fields include title, description, etc., but not ID (non-iterable)
        
        #Instead of __all__, we want to handpick which fields can be altered by the user, when 
        # creating a new project
        
        fields = [ 'title' , 'featured_image' , 'description' , 'demo_link' , 'source_link']
        widgets = {
            'tags' : forms.CheckboxSelectMultiple
        }
        
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class':'input',})
            
        # self.fields['title'].widget.attrs.update(
        #     {'class':'input','placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update(
        #     {'class':'input'})
            

class ReviewForm (ModelForm):
    class Meta:
        model = Review
        fields = [ 'value' , 'body' ]
    
        labels = {
            'value': 'Place your vote' ,
            'body': 'Add a comment with your vote'
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class':'input',})