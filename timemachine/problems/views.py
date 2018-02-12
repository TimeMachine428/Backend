from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from problems.models import Problem
from problems.serializers import ProblemSerializer

@csrf_exempt
def problems_list(request):
    if request.method == 'GET':
        problems = Problem.objects.all()
        serializer = ProblemSerializer(problems, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProblemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def problems_detail(request, pk):
    """
    Retrieve, update or delete a code problem.
    """
    try:
        problem = Problem.objects.get(pk=pk)
    except Problem.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProblemSerializer(problem)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProblemSerializer(problem, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        problem.delete()
        return HttpResponse(status=204)

# Create your views here.
