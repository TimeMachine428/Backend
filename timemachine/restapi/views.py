from rest_framework import generics, permissions
from restapi.models import Problem, Rating, User
from restapi.serializers import ProblemSerializer, RatingSerializer, SolutionSerializer, TestCaseSerializer, \
    UserSerializer
from restapi.permissions import IsOwnerOrReadOnly, IsOwnerOfProblemOrReadOnly
from rest_framework.permissions import AllowAny
from submissions.evaluate import evaluate
from django.contrib.auth.models import AnonymousUser

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (request.user and not isinstance(request.user, AnonymousUser)):
            return True
        return False


class ProblemAPIView(generics.ListCreateAPIView):
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # get
    def get_queryset(self):
        qs = Problem.objects.all()
        username = self.request.GET.get("author")
        if username is not None:
            user = User.objects.get(username=username)
            qs = qs.filter(author=user).distinct()
        return qs

    # post
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProblemRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ProblemSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Problem.objects.all()


class TestCaseAPIView(generics.ListCreateAPIView):
    lookup_field = 'problem_id'
    serializer_class = TestCaseSerializer
    permission_classes = [IsOwnerOfProblemOrReadOnly]

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.test_cases.all()

    def perform_create(self, serializer):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        serializer.save(problem=problem_obj)


class TestCaseRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = TestCaseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.test_cases.all()


class RatingAPIView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = RatingSerializer

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.ratings.all()

    def perform_create(self, serializer):
        problem_id = self.kwargs.get('problem_id')
        problem = Problem.objects.get(pk=problem_id)
        rating = serializer.save(rating_of=problem, reviewer=self.request.user)

        new_rating = rating.rating
        if problem.rating is None:
            problem.rating = new_rating
        else:
            n = problem.ratings.count()
            problem.rating = ((n - 1) * problem.rating + new_rating) / n

        problem.save()


class RatingRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.ratings.all()

    def perform_update(self, serializer):
        old_rating = self.get_object().rating

        problem_id = self.kwargs.get('problem_id')
        problem = Problem.objects.get(pk=problem_id)
        rating = serializer.save(rating_of=problem, reviewer=self.request.user)

        new_rating = rating.rating
        n = problem.ratings.count()

        problem.rating += (new_rating - old_rating) / n
        problem.save()

    def perform_destroy(self, instance):
        problem_id = self.kwargs.get('problem_id')
        problem = Problem.objects.get(pk=problem_id)
        n = problem.ratings.count()

        if n == 1:
            problem.rating = None
        else:
            problem.rating = (n * problem.rating - instance.rating) / (n - 1)

        problem.save()
        super().perform_destroy(instance)


class SolutionRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SolutionSerializer

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.solutions.all()


class SolutionAPIView(generics.ListCreateAPIView):
    serializer_class = SolutionSerializer

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.solutions.all()

    def perform_create(self, serializer):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        instance = serializer.save(author=self.request.user, problem=problem_obj)

        # Submit the solution for evaluation
        evaluate(problem_obj, instance)


# ------------------- added for S14 - save solution ----------------------------------------
class PartialSolutionAPIView(generics.ListCreateAPIView):
    serializer_class = SolutionSerializer

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.partialSolutions.all()

    def perform_create(self, serializer):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        instance = serializer.save(author=self.request.user, problem=problem_obj)

        # Save the partial solution in the database and associate it with the particular author
        savePartial(problem_obj, instance) # TODO: savePartial is not implemented yet


class PartialSolutionRUDView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = SolutionSerializer

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.partialSolutions.all()


class UserAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    model = User
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = User.objects.all()
        username = self.request.GET.get("username")
        # password = self.request.GET.get("password")
        # if username is not None and password is not None:
        #     qs = qs.filter(username=username)
        #     qs = qs.filter(password=password)
        if username is not None:
            qs = qs.filter(username=username).distinct()
        else:
            qs = []
        return qs

    # def perform_create(self, serializer):
    #     serializer.save()


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
