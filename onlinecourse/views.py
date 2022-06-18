from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id
#def submit(request, course_id):


# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
   submitted_anwsers = []
   for key in request.POST:
       if key.startswith('choice'):
           value = request.POST[key]
           choice_id = int(value)
           submitted_anwsers.append(choice_id)
   return submitted_anwsers

def submit(request, course_id):
    submitted_questions= []
    for key in request.POST:
        if key.startswith('question'):
           value = request.POST[key]
           submitted_question = Question.objects.get(id=value)
           submitted_questions.append(submitted_question)
    user = request.user
    course = Course.objects.get(id=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    
    total_num_wrong=0
    num_wrong_choices=0
    
    total_num_correct_choices=0
    for question in submitted_questions:
        num_wrong=0
        num_correct_choices=question.choice_set.filter(correct=True).count()
        submission.question.add(question)
        submission.save()
        answers = extract_answers(request)
        # this function is from the model Question
        # returns a dict with keys [true_not_selected] and [wrong_choices]
        # that hold query sets
        result = question.is_get_score(answers)
        # true_not_selected false_but_selected
        if result['true_not_selected']:
            for item in result['true_not_selected']:
                num_wrong+=1
                print(f'Wrong true not selected:{num_wrong}')
                submission.true_not_selected.add(item)
                submission.save()
        if result['wrong_choices']:
            for item in result['wrong_choices']:
                if num_correct_choices-num_wrong>0:
                    num_wrong+=1
                submission.false_but_selected.add(item)
                submission.save()
        total_num_correct_choices+=num_correct_choices
        total_num_wrong+=num_wrong
        print(f'Total correct choices: {total_num_correct_choices}')
        print(f'Total num wrong:{total_num_wrong}')
        # Score is based on how many correct choices made
        # Each correct choice is a point, a point is deducted
        # For not selecting a correct answer and a point is deducted
        # selecting a wrong choice. Score can be no less than 0.
        num_correct=total_num_correct_choices - total_num_wrong
        print(f'score is {num_correct} out of {total_num_correct_choices}')
        grade=round(num_correct/total_num_correct_choices*100) 
        print(f'Grade is: {grade}')
        submission.grade = grade
        submission.save()
        print(submission.grade)  
    # print(f'TRUE NOT SELECTED:{submission.enrollment}')
    return HttpResponseRedirect(reverse(viewname='onlinecourse:result', args=(course.id, submission.id)))
       
# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
        # Get course and submission based on their ids
        # Get the selected choice ids from the submission record
        # For each selected choice, check if it is a correct answer or not
        # Calculate the total score
def show_exam_result(request, course_id, submission_id):
    course = Course.objects.get(id=course_id)
    submission = Submission.objects.get(id=submission_id)
    grade=submission.grade
    context={"grade":grade,
             "course":course,
             "submission":submission,}
    return render(request,'onlinecourse/exam_result_bootstrap.html', context)    



