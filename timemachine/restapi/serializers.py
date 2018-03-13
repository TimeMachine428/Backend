from rest_framework import serializers
from restapi.models import Problem, Rating, Solution, User
from submissions.serializers import JobSerializer, TestCaseSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'github_id', 'is_staff', 'password')


class ProblemSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)
    pub_date = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField(default=5)

    class Meta:
        model = Problem
        fields = ('id', 'title', 'author', 'test_cases', 'description', 'difficulty', 'rating', 'pub_date')


class RatingSerializer(serializers.ModelSerializer):
    rating_of = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = UserSerializer(read_only=True)
    date = serializers.ReadOnlyField()

    class Meta:
        model = Rating
        fields = ('id', 'message', 'rating', 'date', 'content', 'rating_of', 'reviewer')


class SolutionSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    output = serializers.ReadOnlyField(default="")

    class Meta:
        model = Solution
        fields = ('id', 'created', 'code', 'language', 'output', 'jobs', 'author')
