from django.urls import reverse
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from restapi.models import User, Problem, TestCase, Rating, Solution
from timemachine.tests import JWTAPITestCase
from submissions.jobs import TestCaseJob

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class ProblemAPITestCase(JWTAPITestCase):

    def setUp(self):
        # Set up a test user
        user = User(email="test@test.com", username="Test")
        user.set_password("TEST")
        user.save()

        # Set up an author
        author = User(email="test@author.com", username="TestAuthor")
        author.set_password("TEST")
        author.save()

        # Test problem
        self.problem = Problem(title="Factorial",
                               author=author,
                               description="Write the factorial function fact(n)",
                               difficulty=1)
        self.problem.save()

    def test_retrieve(self):
        uri = self.problem.get_absolute_url()
        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_problem_list(self):
        uri = reverse('restapi:problems-listcreate')
        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Problem.objects.count(), len(response.data))

    def test_post_problem(self):
        uri = reverse("restapi:problems-listcreate")
        data = {
            "title": "Test",
            "description": "Testing things",
            "difficulty": 4,
        }

        # Test without authentication
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="User needs to be authenticated to post")

        # Test with authentication
        self.authenticate(User.objects.first())
        response = self.client.post(uri, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg="Authenticated user should be able to post")
        self.assertEqual(Problem.objects.count(), 2)
        self.assertEqual(Problem.objects.last().author, User.objects.first(),
                         msg="The authenticated user should be the author of the new post")

    def test_update_problem(self):
        problem = Problem.objects.first()

        uri = problem.get_absolute_url()
        data = {
            "title": "Factorial",
            "description": "New description",
            "difficulty": 2,
        }

        self.authenticate(User.objects.first())
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg="Only the author of the problem should be able to modify it")

        self.authenticate(problem.author)
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg="The author should be able to modify the problem")
        self.assertEqual(Problem.objects.first().description, data["description"],
                         msg="The description should've been updated")

    def test_delete_problem(self):
        initial_count = Problem.objects.count()
        problem = Problem.objects.first()
        url = problem.get_absolute_url()

        self.authenticate(User.objects.first())
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg="Only the author should be able to delete a problem")

        self.authenticate(problem.author)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         msg="The author should be able to delete a problem")

        self.assertEqual(Problem.objects.count(), initial_count - 1)
        return problem


class TestCaseAPITestCase(JWTAPITestCase):

    def setUp(self):
        # Set up a test user
        self.user = User(email="test@test.com", username="Test")
        self.user.set_password("TEST")
        self.user.save()

        # Set up an author
        self.author = User(email="test@author.com", username="TestAuthor")
        self.author.set_password("TEST")
        self.author.save()

        # Test problem
        self.problem = Problem(title="Factorial",
                               author=self.author,
                               description="Write the factorial function fact(n)",
                               difficulty=1)
        self.problem.save()

        test_case = TestCase(method="fact", inputs="[5]", outputs="[120]", problem=self.problem)
        test_case.save()

    def test_list_create(self):
        uri = reverse('restapi:testcases-listcreate', kwargs={'problem_id': self.problem.pk})

        # Test creation
        data = {
            "method": "fact",
            "inputs": "[4]",
            "outputs": "[24]",
        }
        self.authenticate(self.user)
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg="Only the author of the problem should be able to add test cases")

        self.authenticate(self.author)
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg="The author should be able to successfully create the test case")

        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(len(response.data), 2, msg="There should now be two list entries")

    def test_retrieve(self):
        test_case = TestCase.objects.first()
        uri = test_case.get_absolute_url()

        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(test_case.id, response.data["id"])

    def test_update(self):
        test_case = TestCase.objects.first()
        url = test_case.get_absolute_url()

        data = {
            "method": "fact",
            "input": "[0]",
            "output": "[1]",
        }
        self.authenticate(self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.author)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        test_case = TestCase.objects.first()
        url = test_case.get_absolute_url()

        self.authenticate(self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate(self.author)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RatingAPITestCase(JWTAPITestCase):

    def setUp(self):
        # Set up a test user
        self.user = User(email="test@test.com", username="Test")
        self.user.set_password("TEST")
        self.user.save()

        # Set up an author
        self.author = User(email="test@author.com", username="TestAuthor")
        self.author.set_password("TEST")
        self.author.save()

        # Test problem
        self.problem = Problem(title="Factorial",
                               author=self.author,
                               description="Write the factorial function fact(n)",
                               difficulty=1)
        self.problem.rating = 5  # Manually set this
        self.problem.save()

        self.rating = Rating(message="Hello", rating=5, content="Awesome Sauce", rating_of=self.problem, reviewer=self.user)
        self.rating.save()

    def test_listcreate(self):
        uri = reverse('restapi:ratings-listcreate', kwargs={'problem_id': self.problem.pk})

        # Test creation
        data = {
            "message": "Hi",
            "rating": 3,
            "content": "This is pretty cool dude",
        }
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         msg="User should be authenticated before being able to rate problems")

        self.authenticate(self.user)
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg="An authenticated user should be able to rate problems")

        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(len(response.data), 2, msg="There should now be two list entries")

        # Test that the ratings have averaged out
        self.assertAlmostEqual(Problem.objects.first().rating, 4)

    def test_retrieve(self):
        rating = Rating.objects.first()
        uri = rating.get_absolute_url()

        response = self.client.get(uri, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], rating.id)

    def test_update(self):
        rating = Rating.objects.first()
        uri = rating.get_absolute_url()

        self.authenticate(self.author)

        data = {
            "message": "Hello",
            "rating": 2,
            "content": "Not so awesome sauce",
        }
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg="Only the reviewer should be able to update a rating")

        self.authenticate(self.user)
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg="The reviewer should be able to update his rating")

        self.assertAlmostEqual(Problem.objects.first().rating, 2,
                               msg="The rating of the problem should've been updated to 2")

    def test_delete(self):
        rating = Rating.objects.first()
        uri = rating.get_absolute_url()

        self.authenticate(self.author)
        response = self.client.delete(uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         msg="Only the reviewer should be able to delete a rating")

        self.authenticate(self.user)
        response = self.client.delete(uri, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         msg="The review should be able to delete their rating")

        self.assertIsNone(Problem.objects.first().rating,
                          msg="The problem rating should be made Null since there are no more ratings")

    def test_running_average(self):
        # Reset everything
        Rating.objects.first().delete()
        Problem.objects.first().rating = None

        url = reverse("restapi:ratings-listcreate", kwargs={'problem_id': Problem.objects.first().id})

        self.authenticate(self.user)

        template = {
            "message": "Hi",
            "rating": 5,
            "content": "Yo nice job on this problem it's awesome",
        }
        self.client.post(url, data=template, format='json')
        self.assertAlmostEqual(Problem.objects.first().rating, 5)

        template["rating"] = 1
        self.client.post(url, data=template, format='json')
        self.assertAlmostEqual(Problem.objects.first().rating, 3)

        template["rating"] = 2
        self.client.post(url, data=template, format='json')
        self.assertAlmostEqual(Problem.objects.first().rating, 8 / 3)

        # Change the 2nd rating to 2, average should go to 9 / 3 = 3
        put_url = Rating.objects.all()[1].get_absolute_url()
        self.client.put(put_url, data=template, format='json')
        self.assertAlmostEqual(Problem.objects.first().rating, 3)

        # Delete the 1st rating, average should go to 4 / 2 = 2
        delete_url = Rating.objects.first().get_absolute_url()
        self.client.delete(delete_url, format='json')
        self.assertAlmostEqual(Problem.objects.first().rating, 2)


class SolutionsAPITestCase(JWTAPITestCase):

    def setUp(self):
        # Set up a test user
        self.user = User(email="test@test.com", username="Test")
        self.user.set_password("TEST")
        self.user.save()

        # Set up an author
        self.author = User(email="test@author.com", username="TestAuthor")
        self.author.set_password("TEST")
        self.author.save()

        # Test problem
        self.problem = Problem(title="Factorial",
                               author=self.author,
                               description="Write the factorial function fact(n)",
                               difficulty=1)
        self.problem.save()

        test_case = TestCase(method="fact", inputs="[5]", outputs="[120]", problem=self.problem)
        test_case.save()

        test_case2 = TestCase(method="fact", inputs="[0]", outputs="[1]", problem=self.problem)
        test_case2.save()

        test_case3 = TestCase(method="fact", inputs="[4]", outputs="[24]", problem=self.problem)
        test_case3.save()

    def test_create(self):
        url = reverse("restapi:solutions-listcreate", kwargs={"problem_id": self.problem.id})

        # Authenticate as a user
        self.authenticate(self.user)

        # Submit the following solution
        data = {
            "code": """
def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)

            """
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        solution = Solution.objects.first()
        self.assertIsNotNone(solution, msg="A solution object should've been created")

        # There should be one job for each test case return in response.data
        self.assertEqual(len(response.data["jobs"]), 3, msg="There should be one job planned")

        jobs = TestCaseJob.objects.filter(job_ptr__solution=solution)

        # Manually run all jobs (without RQ)
        for job in jobs:
            self.assertIsInstance(job, TestCaseJob)
            job.run()
            self.assertTrue(job.success)

    def test_retrieve(self):
        solution = Solution(code="Blah", language="python", problem=self.problem)
        solution.save()

        url = solution.get_absolute_url()
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
