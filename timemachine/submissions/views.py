from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Job, TestCaseJob
from restapi.models import Problem, Solution
from restapi.serializers import SolutionSerializer


@api_view(['PUT'])
def submit(request):
    problem_id = request.data.get('problem_id')
    problem = Problem.objects.get(pk=problem_id)
    code = request.data.get('code')
    test_cases = problem.testcase_set.all()

    # TODO: Incorporate authentication to have a solution author
    solution = Solution()
    solution.code = code
    solution.language = problem.programming_language
    solution.save()

    jobs = []
    for test_case in test_cases:
        job = TestCaseJob()
        job.solution = solution
        job.testcase = test_case
        job.name = "%s: (%d, %d)" % (problem.title, job.solution_id, test_case.id)
        job.save()

        # Enqueue the job to be run using RQ
        job.enqueue()
        jobs.append(job)

    serializer = SolutionSerializer(solution)
    return Response(serializer.data)


def get_job(request):
    # just a test

    job = Job.objects.get(pk=int(request.GET.get('job_id')))
    return JsonResponse(model_to_dict(job))
