import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


def create_question(text, days=0):
    """Creates a question with the given question_text, and published the given number of days
    - Negative for a date in the past
    - Positive por questions with a future date
    """
    publish_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=publish_date)


class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = create_question("Test question")

    def test_was_published_recently_with_future_question(self):
        """Was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time

        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Was_published_recently returns True for question whose pub_date is a few hours old"""
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date = time

        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        """Was_published_recently returns False for question whose pub_date is more than 1 day old"""
        time = timezone.now() - datetime.timedelta(days=2)
        self.question.pub_date = time

        self.assertIs(self.question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):
    questions_list_name = "latest_question_list"

    def test_no_questions(self):
        """If no questions exist, a message is displayed"""
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[self.questions_list_name], [])

    def test_ignore_future_questions(self):
        """Ignore all the questions with a future pub_date"""
        create_question("Test question", 2)

        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[self.questions_list_name], [])

    def test_shows_past_questions(self):
        """Shows questions with a past pub_date"""
        question1 = create_question("Test question", -1)
        question2 = create_question("Test question 2", -2)

        response = self.client.get(reverse("polls:index"))
        self.assertNotContains(response, "No polls are available.")
        self.assertIn(question1, response.context[self.questions_list_name])
        self.assertIn(question2, response.context[self.questions_list_name])

    def test_future_question_and_past_question(self):
        """Shows the question with a past pub_date while ignoring the question with a future pub_date"""
        past_question = create_question("Past question", -1)
        future_question = create_question("Future question", 1)

        response = self.client.get(reverse("polls:index"))
        self.assertNotContains(response, "No polls are available.")
        self.assertIn(past_question, response.context[self.questions_list_name])
        self.assertNotIn(future_question, response.context[self.questions_list_name])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """Returns 4040 on question with pub_date in the future"""
        future_question = create_question("Future question", 1)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Shows the  question with a pub_date in the past"""
        past_question = create_question("Past question", -1)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)
