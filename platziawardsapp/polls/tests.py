import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question("Test question?")

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
    def test_no_questions(self):
        """If no questions exist, a message is displayed"""
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
