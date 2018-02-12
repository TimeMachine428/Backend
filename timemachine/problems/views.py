from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from problems.models import Problem
from problems.serializers import ProblemSerializer


@api_view(['GET', 'POST'])
def problems_list(request, format=None):
    if request.method == 'GET':
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def problems_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code problem.
    """
    try:
        problem = Problem.objects.get(pk=pk)
    except Problem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProblemSerializer(problem)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProblemSerializer(problem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        problem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
