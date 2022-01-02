from enum import unique
from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
        # if a user gets deleted, then its profile also gets deleted
    
    username = models.CharField(max_length=200, blank=True, null=True)
    
    location = models.CharField(max_length=200, blank=True, null=True)
    
    name = models.CharField(max_length=200, blank=True, null=True)
    
    email = models.EmailField(max_length=500, blank=True, null= True)
    
    short_intro = models.CharField(max_length=500, blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True)
    
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True, default='profiles/user-default.png')
        # instead of static/images, upload this to static/images/profiles (stores the profile pictures)
        # the defualt picture is now : static/images/profiles/user-default.png (static/images path is already accounted for, so just add the rest)
    
    social_github = models.CharField(max_length=200, blank=True, null= True)
    social_twitter = models.CharField(max_length=200, blank=True, null= True)
    social_linkedin = models.CharField(max_length=200, blank=True, null= True)
    social_youtube = models.CharField(max_length=200, blank=True, null= True)
    social_website = models.CharField(max_length=200, blank=True, null= True)
    social_instagram = models.CharField(max_length=200, blank=True, null= True)
        # These are all the various links, the user might want to display on its profile
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.username
    

class Skill (models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
        # .CASCADE: Whenever a profile gets deleted, all the skills related to it, also get deleted
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__ (self):
        return self.name


class Message (models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
        # on_delete=models.SET_NULL :If the sender deletes their account, the message should still remain in the receiver's inbox.
        # null=True: If someone doesn't have an account, then they'll still be sending the message, but the sender field will be NULL (anonymous user lol), as it won't connect as foreign key to any 'profile'
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    
    name = models.CharField(max_length= 200, null= True, blank= True)

    email = models.EmailField(max_length= 200, null= True, blank= True)
    subject = models.CharField(max_length= 200, null= True, blank= True)
    body = models.TextField()       # No blank=True, as the body SHOULD have some content
    
    is_read = models.BooleanField(default= False, null= True)
    
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default= uuid.uuid4, unique= True, primary_key= True, editable= False)
    
    
    def __str__ (self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']