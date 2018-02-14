from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Job, TestCaseJob


test_code = """

def fact(n):
    if n <= 1:
        return 1

    return n * fact(n-1)

"""


def submit(request):
    # Just a test for now
    job = TestCaseJob()
    job.name = 'test_job'
    job.code = test_code
    job.method = 'fact'
    job.metadata = """
    { "args": [4], "kwargs": {}, "result": 24 }
    """

    job.save()
    job.enqueue()

    return JsonResponse(data={
        "job_id": job.id
    })


def get_job(request):
    # just a test

    job = Job.objects.get(pk=int(request.GET.get('job_id')))
    return JsonResponse(model_to_dict(job))
