from rest_framework import generics
from restapi.models import Problem
from restapi.serializers import ProblemSerializer, RatingSerializer, SolutionSerializer, TestCaseSerializer
from restapi.permissions import IsOwnerOrReadOnly
from submissions.evaluate import evaluate


class ProblemAPIView(generics.ListCreateAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProblemRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ProblemSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Problem.objects.all()


class TestCaseAPIView(generics.ListCreateAPIView):
    serializer_class = TestCaseSerializer

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
        problem_obj = Problem.objects.get(pk=problem_id)
        serializer.save(review_of=problem_obj, reviewer=self.request.user)


class RatingRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        problem_id = self.kwargs.get('problem_id')
        problem_obj = Problem.objects.get(pk=problem_id)
        return problem_obj.ratings.all()


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
