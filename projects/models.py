from enum import unique
from django.db import models
import uuid             # uuid is a module ; Used in the 'id' column
from users.models import Profile

# Create your models here.

# Here, we'll create our classes that will be used to represent tables.


"""First Model"""
class Project(models.Model):    # We're in the project app
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    
    title = models.CharField(max_length=200)    # This is a 'small amt of text' field
    description = models.TextField(null=True , blank=True)   # We're allowed to create a new 'object' while being able to leave this field blank, null by default, is set to false.
                                                             # 'blank=true' means we're allowed to submit a form with this value being empty
    
    featured_image = models.ImageField(null=True , blank=True , default = "default.jpg")
    
    demo_link = models.CharField(max_length=2000,blank=True)
    source_link = models.CharField(max_length=2000 , null=True , blank=True)    # Not all the fields may have a source code link
    
    # Creating a many to many link between the two tables 'tag' and 'project'
    tags = models.ManyToManyField('Tag',blank=True) # Tag is in quotes ('Tag'), because we've defined the class Tag below the class Project, so this is like using a reference. Kind of like how we have to write function declaration at the top, if the function being referenced is defined below the current function
    
    # We also want to store the variable 'votes', which is defined in the 'Review' class
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)   # Whenever we create the field, just automatically generate our timestamp. So, it'll create it automatically, we don't have to worry about it
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)  # This has to be unique ; Set this as the primary key of the table/database ; This can't be editted by anyone
    
    # Add a method that is part of the class, this returns the value below 'self.title' where we see the name of the table, on the admin page of our wesite
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total' , 'title']   # Order in the descending order of 'vote ratio', and if 'vote_ratios' are the same, then sort in the descending order of total votes. And if those two also match, then order in the alphabetical order (increasing order of 'title')
        
    @property
    def getVoteCount (self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes/totalVotes)*100    # Conver this to a valid percentage
        
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
        self.save()
        
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
        
# CharField, TextField, DateTimeField, and UUIDField are all classes in the 'models' module of Python


"""Second Model"""
class Review(models.Model):
    
    VOTE_TYPE = (                   # VOTE_TYPE is a tuple of tuples
        ( 'up' , 'Up Vote' ),       # First Tuple
        ( 'down' , 'Down Vote' ),   # Second Tuple
    )
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)  # There are two parts to this
    # models.foreignkey : This table will store info which is related to the main table above this 'Project' which stores the users.
    # on_delete: Tells what happens to the data stored in this table for a user, if that user gets deleted in the main table. In this case, we'll set the field related to that user to NULL.
    # but if we use CASCADE, it will just delete the respective field for that user. (It will delete all the 'reviews' if the 'Project' is deleted)
    
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE)  # We'll get a drop down list, with the choices being 'upvote' and 'downvote'
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    class Meta:
        unique_together = [
            ['owner' , 'project'],   # No instance of the review can have the same project and the same owner, ie, no person can comment on the same project twice (to avoid cheating)
        ]
    
    def __str__(self) -> str:
        return self.value
    

"""Third Model"""
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self) -> str:
        return self.name
