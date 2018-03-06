from .models import TestCaseJob


def evaluate(problem, solution):
    for test_case in problem.test_cases.all():
        job = TestCaseJob()
        job.solution = solution
        job.testcase = test_case
        job.name = "%s: (%d, %d)" % (problem.title, job.solution_id, test_case.id)
        job.save()

        # Enqueue the job to be run using RQ
        job.enqueue()
