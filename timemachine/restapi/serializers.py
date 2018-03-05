from rest_framework import serializers
from restapi.models import Problem, Rating, Solution, TestCase
from submissions.serializers import JobSerializer


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name', 'author', 'description', 'difficulty', 'good')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'title', 'date', 'rating', 'content')


class SolutionSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Solution
        fields = ('id', 'created', 'code', 'language', 'output', 'jobs')


class TestCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestCase
        fields = ('id', 'method', 'inputs', 'outputs')
