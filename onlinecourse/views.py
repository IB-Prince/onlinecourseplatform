from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LessonForm, QuestionForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
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
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
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
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = self.object
        context['is_enrolled'] = False
        if user.is_authenticated:
            context['is_enrolled'] = check_if_enrolled(user, course)
        return context

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled:
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course_id,)))

@login_required    
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission_id = submission.id
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course_id, submission_id)))


def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers

@login_required
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, id=submission_id, enrollment__user=request.user, enrollment__course=course)
    questions = Question.objects.filter(course=course)

    total_grade_points = sum(question.grade for question in questions)
    selected_choices = list(submission.choices.all())
    choices_by_q = {}
    for ch in selected_choices:
        choices_by_q.setdefault(ch.question_id, []).append(ch.id)
    
    total_score = 0
    for question in questions:
        selected_ids = choices_by_q.get(question.id, [])
        if question.is_get_score(selected_ids):
            total_score += question.grade

    if total_grade_points > 0:
        percentage_score = (total_score / total_grade_points) * 100
    else:
        percentage_score = 0
    context['course'] = course
    context['grade'] = total_score
    context['percentage_score'] = percentage_score
    context['choices'] = submission.choices.all()

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

def _user_is_instructor_of_course(user, course):
    if not user.is_authenticated:
        return False
    # Check via the Course.instructor m2m relation
    return course.instructor.filter(user=user).exists()

@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not _user_is_instructor_of_course(request.user, course):
        return HttpResponseForbidden("You are not an instructor of this course.")
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('onlinecourse:course_details', pk=course.id)
    else:
        form = LessonForm()
    return render(request, 'onlinecourse/instructor_add_lesson.html', { 'course': course, 'form': form })

@login_required
def add_question(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not _user_is_instructor_of_course(request.user, course):
        return HttpResponseForbidden("You are not an instructor of this course.")
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course
            question.save()
            return redirect('onlinecourse:course_details', pk=course.id)
    else:
        form = QuestionForm()
    return render(request, 'onlinecourse/instructor_add_question.html', { 'course': course, 'form': form })