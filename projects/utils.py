from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:        # First try this, and if it fails, go to the 'except'
        projects = paginator.page(page)
    except PageNotAnInteger:
        page  = 1               # If no 'integer/valid' page (page no.) is passed in, set the default page no. to 1 (1st page)
        projects = paginator.page(page)
    except EmptyPage:   # Let's say someone goes to page 99 somehow, but there aren't so many projects, so instead django will do the following
        page = paginator.num_pages      # paginator.num_pages gives us the last page (num_pages, returns the total no. of pages in the paginator)
        projects = paginator.page(page)
        
    leftIndex = ((int)(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = ((int)(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
        
    custom_range = range(leftIndex,rightIndex)
    
    return custom_range, projects

def searchProjects(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return projects, search_query   