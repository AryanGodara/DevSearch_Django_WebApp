from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        {'GET':'/api/projects'},             #? This will return back a list of project objects
        {'GET':'/api/projects/id'},          #? This will return back a single project
        {'POST':'/api/projects/id/vote'},    #? The path where someone who wants to vote is sent
        
        {'POST':'/api/users/token'},         #? To log in users
        {'POST':'/api/users/token/refresh'}  #TODO Has something to do with making sure that the user stays logged in. More info later maybe lol
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)    # This serializer takes the queryset('projects' is a queryset), and converts it to JSON data ; many=True, means that we're serializing many objects lol. If it was a single project, then we wouldn't set many to True
    
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    
    review.value = data['value']
    review.save()
    project.getVoteCount
    

    serializer = ProjectSerializer(project, many=False)
        
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagID = request.data['tag']
    projectID = request.data['project']
    
    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)
    
    project.tags.remove(tag)
    
    return Response('Tag was deleted!')