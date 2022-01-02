from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
        #* Now, instead of the 'owner' field of the model 'Project' return a 'profile ID', will instead return the entire profile object
    tags = TagSerializer(many=True)
        #* Just did the same thing for tags. And many is set to True, as there can be multiple tags
    
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        
    def get_reviews(self, obj):       # 'self' here doesn't refer to the 'model project', but instead it refers to the 'SerializerMethodField class'
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        
        return serializer.data