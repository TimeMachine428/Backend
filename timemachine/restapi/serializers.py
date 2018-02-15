from rest_framework import serializers
from restapi.models import Problem, Rating, Solution


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'title', 'author', 'description', 'difficulty', 'rating', 'programming_language', 'solution', 'pub_date')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'message', 'date', 'rating', 'content')


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('id', 'created', 'code', 'language', 'output', 'pending')
