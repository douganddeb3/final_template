# from django.test import TestCase
# from django.test import Client, TestCase
# from .models import Instructor, Learner, Course, Lesson, Enrollment, Question, Choice, Submission
# import os
# import pathlib
# import unittest
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
# Create your tests here.
# c = Client(). // simulate requests 
# response = c.get(“/flights/“) or (f”/flights/”{f.id}”)
# self.assertEqual(response.status_code, 200)
# self.assertEqual(response.context[“flights”].count(), 3)
# pip3 install webdriver-manager
# pip3 install selenium
# def file_uri(filename):
# 	return pathlib.Path((os.path.abspath(filename)).as_uri()  // need uri in order to open it up
# driver = webdriver.Chrome(ChromeDriverManager().install())
# The same can be used to set Firefox, Edge and ie binaries.

# 	driver = webdriver.Chrome()

# tests.py
# class WebPageTests(unittest.TestCase):

# 	def test_title(self):
# 		driver.get(file_uri(“counter.html”))
# 		self.assertEqual(driver.title, “Count”)
# self.assertEqual(driver.find_element_by_tag_name(“h1”).text, “1”)
# assertEqual
# assertNotEqual
# assertTrue
# assertFalse
# assertIn
# assertNotIn
# def test_increase(self):
# 	driver.get(file_uri(“counter.html”))
# 	increase = driver.find_element_by_id(“increase”)
# 	increase.click()

# class ExamTestCase(TestCase):
# 	## separate test db, setUp is a special function
# 	def setUp(self):
# 		a1 = Airport.objects.create(code=“AAA”, city=“City 1”)



# python manage.py test
