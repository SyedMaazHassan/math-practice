from django.db.models import query
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json

# main page function


def save_exercise(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        image = None
        if 'img' in request.FILES:
            image = request.FILES['img']
        exercise_name = request.POST['exercise-name']
        exercise_description = request.POST['exercise-description']
        created_by = request.user
        my_topic = None
        if 'topic' in request.POST:
            topic_id = request.POST['topic']
            if topic_id:
                my_topic = topic.objects.get(id=topic_id)

        new_exercise = exercise(
            name=exercise_name,
            description=exercise_description,
            image=image,
            topic=my_topic,
            created_by=created_by,
        )
        new_exercise.save()
        messages.info(request, "New exercise has been created successfully!")

    return redirect("index")


def view_question(request, question_id):
    # if not request.user.is_authenticated:
    #     return redirect("login")
    focused_question = question.objects.get(id=int(question_id))
    # copy_of_expression = focused_question.criteria

    question_version_list = focused_question.get_question_versions()
    print(question_version_list)

    # 1 = edited expression
    # 2 = values (form values if required)

    # for single_question_element in focused_question.question_elements.all():
    #     value = single_question_element.value if single_question_element.value else "?"

    #     focused_question.criteria = focused_question.criteria.replace(
    #         single_question_element.symbol,
    #         value
    #     )

    context = {
        'answers_fields': focused_question.question_elements.filter(nature="answer"),
        'versions': question_version_list,
        'question': focused_question
    }
    return render(request, "attempt.html", context)


def complete_question(request):
    if not request.user.is_authenticated:
        return None

    output = {
        'status': True,
    }
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET['id'])

        focused_question = question.objects.get(id=id)
        focused_question.is_completed = True
        focused_question.save()

        # print(question_element_list, type(question_element_list))

    return JsonResponse(output)


def save_loop(request):
    if not request.user.is_authenticated:
        return None

    output = {
        'status': True,
    }
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET['id'])
        loop = int(request.GET['loop'])
        success_message = request.GET['success_message']
        failure_message = request.GET['failure_message']

        focused_question = question.objects.get(id=id)
        focused_question.loop = loop
        focused_question.success_message = success_message
        focused_question.failure_message = failure_message
        focused_question.save()

        # print(question_element_list, type(question_element_list))

    return JsonResponse(output)


def save_rule(request):
    if not request.user.is_authenticated:
        return None

    output = {
        'status': True,
    }
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET['id'])
        criteria = request.GET['criteria']

        focused_question = question.objects.get(id=id)
        focused_question.criteria = criteria
        focused_question.save()

        # print(question_element_list, type(question_element_list))

    return JsonResponse(output)


def save_question_elements(request):
    if not request.user.is_authenticated:
        return None

    output = {
        'status': True,
    }
    if request.method == "GET" and request.is_ajax():
        id = int(request.GET['id'])
        question_element_list = json.loads(
            request.GET['question_element_list'])

        focused_question = question.objects.get(id=id)
        focused_question.question_elements.all().delete()

        for question_element in question_element_list:
            # print(question_element)
            new_question_element = focused_question.question_elements.create(
                label=question_element['label'],
                key=question_element['key'],
                symbol=question_element['expression_symbol'],
                nature=question_element['nature'],
                data_type=question_element['type'],
                value=question_element['value'],
                is_random=question_element['is_random'],
                example_value=question_element['example_value']
            )

            for single_condition in question_element['condition_list']:
                new_question_element.conditions.create(
                    key=single_condition['key'],
                    limit=single_condition['limit'],
                    query=single_condition['value']
                )

        # print(question_element_list, type(question_element_list))

    return JsonResponse(output)


def save_question(request):
    if not request.user.is_authenticated:
        return None

    output = {
        'status': True,
        'new_question_id': None
    }

    if request.method == "GET" and request.is_ajax():
        id = None
        my_exercise = None
        my_topic = None
        if 'id' in request.GET:
            id = int(request.GET['id'])

        if 'exercise_id' in request.GET:
            exercise_id = request.GET['exercise_id']
            if exercise_id:
                exercise_id = int(exercise_id)
                my_exercise = exercise.objects.get(id=exercise_id)
        if 'topic_id' in request.GET:
            topic_id = request.GET['topic_id']
            if topic_id:
                topic_id = int(topic_id)
                my_topic = topic.objects.get(id=topic_id)

        title = request.GET['title']
        description = request.GET['description']

        if id:
            my_question = question.objects.get(id=id)
        else:
            my_question = question()

        my_question.title = title
        my_question.topic = my_topic
        my_question.exercise = my_exercise
        my_question.description = description
        my_question.created_by = request.user
        my_question.save()

        output['new_question_id'] = my_question.id

    return JsonResponse(output)


def add_question(request):
    if request.user.is_authenticated:

        context = {
            'topic_list': topic.objects.all(),
            'exercise_list': exercise.objects.filter(created_by=request.user)
        }

        return render(request, "add-question.html", context)
    return redirect("login")


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {
        'all_exercises': exercise.objects.filter(created_by=request.user).count(),
        'all_questions': question.objects.filter(created_by=request.user, is_completed=True).count()
    }
    return render(request, 'profile.html', context)

# function for signup


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "register-email"
                context['section'] = "register"
                return render(request, "index.html", context)

            user = User.objects.create_user(
                username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            messages.info(
                request, "Your account has been created successfully!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword does not match!")
            context['border'] = "register-password"
            context['section'] = "register"
            return render(request, "index.html", context)

    context = {'section': 'register'}
    return render(request, "index.html", context)


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['login_email']
        password = request.POST['login_password']
        context = {
            'login_email': email,
            'login_password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            context['section'] = "login"
            messages.info(request, "Incorrect login details!")
            return render(request, "index.html", context)
            # return redirect("login")
    else:
        context = {'section': 'login'}
        return render(request, "index.html", context)


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")
