from django.db.models import Q

from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try:        # First try this, and if it fails, go to the 'except'
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page  = 1               # If no 'integer/valid' page (page no.) is passed in, set the default page no. to 1 (1st page)
        profiles = paginator.page(page)
    except EmptyPage:   # Let's say someone goes to page 99 somehow, but there aren't so many profiles, so instead django will do the following
        page = paginator.num_pages      # paginator.num_pages gives us the last page (num_pages, returns the total no. of pages in the paginator)
        profiles = paginator.page(page)
        
    leftIndex = ((int)(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = ((int)(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
        
    custom_range = range(leftIndex,rightIndex)
    
    return custom_range, profiles

def searchProfiles(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)
    
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) |
        Q(bio__icontains=search_query) | Q(skill__in=skills)
    )
    
    return profiles, search_query    