from rest_framework import serializers
from restapi.models import Problem, Rating, Solution, User, PartialSolution
from submissions.serializers import JobSerializer, TestCaseSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'github_id', 'is_staff', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    # def restore_object(self, attrs, instance=None):
    #     user = super(UserSerializer, self).restore_object(attrs, instance)
    #     user.set_password(attrs['password'])
    #     return user

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   # email=validated_data['email']
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProblemSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)
    pub_date = serializers.ReadOnlyField()
    rating = serializers.IntegerField(default=0)
    author_username = serializers.ReadOnlyField()

    class Meta:
        model = Problem
        fields = ('id', 'title', 'author', 'author_username', 'test_cases', 'description', 'difficulty', 'rating', 'pub_date')


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


# added for S14
class PartialSolutionSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    output = serializers.ReadOnlyField(default="")

    class Meta:
        model = PartialSolution
        fields = ('id', 'created', 'modified', 'code', 'language', 'output', 'jobs', 'author')
