import os
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from . import database
from .models import *
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, addHobbiesForm, viewHobbiesForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
import datetime
import json
from collections import Counter
from django.contrib.auth.decorators import login_required
# Create your views here.


def registerPage(request):

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'User created for' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'hobbiesApp/register.html', context)


def loginPage(request):

    if request.method == 'POST':
        # here we are fetching the fieldnames from login form on login.html
        username = request.POST.get('username')
        password = request.POST.get('password')

        # this is djangos method to automatically verify(authenticate) the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'hobbiesApp/profile.html')

    context = {}
    return render(request, 'hobbiesApp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())


def test(request):

    return render(request, 'hobbiesApp/testPage.html')


@login_required(login_url='login')
def profile(request):
    user = MyUser.objects.get(username=request.user)
    print('The user is:' + str(user))
    image = user.image
    email = user.email
    city = user.city
    dob = user.dob
    editing = False
    today = datetime.date.today()
    age = today.year - dob.year - \
        ((today.month, today.day) < (dob.month, dob.day))
    context = {'user': user, 'image': image,
               'city': city, 'dob': dob, 'age': age, 'editing': editing}
    return render(request, 'hobbiesApp/profile.html', context)


@login_required(login_url='login')
def hobbies(request):

    hobby = Hobby.objects.all()
    user = MyUser.objects.get(username=request.user)
    user.save()
    form = addHobbiesForm()
    form2 = viewHobbiesForm()

    if request.method == 'POST' and 'addHobby' in request.POST:
        form = addHobbiesForm(request.POST)
        if form.is_valid():

            # we need the ID to add it onto the users hobby fields
            hobbyID = form.save()

            user.hobbies.add(hobbyID.id)
            form.save()
            return redirect('/hobbies/')

    if request.method == 'POST' and 'addHobbyToUser' in request.POST:
        hobby_selected = request.POST.get('hobbySelected')
        # user.hobbies.add(hobby_selected)
        print(hobby_selected)  # this needs to be id!!!

        return redirect('/hobbies/')

    context = {'form': form, 'form2': form, 'hobby': hobby}

    return render(request, 'hobbiesApp/hobbies.html', context)


@login_required(login_url='login')
def user_api(request, id=None):
    if request.method == "GET":
        return JsonResponse({
            'user': (MyUser.objects.get(username=request.user)).to_dict()
        })

    if request.method == "PUT":
        user = get_object_or_404(MyUser, id=id)
        PUT = json.loads(request.body)
        user.email = PUT['email']
        user.city = PUT['city']
        user.dob = PUT['dob']
        user.hobbies.clear()
        hobbies = PUT['hobbies']
        for hobby in hobbies:
            user.hobbies.add(Hobby.objects.get(name=hobby))

        user.save()
        return JsonResponse({})

    if request.method == "DELETE":
        user = get_object_or_404(MyUser, id=id)
        user.delete()
        return JsonResponse({})

    return HttpResponseBadRequest("Invalid request method")

####


@login_required(login_url='login')
def hobbies_api(request):
    # data = serializers.serialize('json', Hobby.objects.all())
    return JsonResponse({
        'hobbies': [hobby.__str__() for hobby in Hobby.objects.all()]
    })


@login_required(login_url='login')
def send_friend_request(request):
    from_user = request.user
    userID = json.loads(request.body)['userID']
    to_user = MyUser.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')


@login_required(login_url='login')
def accept_friend_request(request):
    jsonbody = (json.loads(request.body))
    friend_request = Friend_Request.objects.get(
        from_user=jsonbody['from_user'], to_user=jsonbody['to_user'])
    if request.method == 'DELETE':
        friend_request.delete()
        return HttpResponse('friend request deleted')
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')


@login_required(login_url='login')
def friend_request_api(request):
    try:
        return JsonResponse({
            'requests': [request.to_dict() for request in Friend_Request.objects.filter(to_user=request.user.id)]
        })
    except Friend_Request.DoesNotExist:
        return JsonResponse({})


def commonhobbies(request):

    context = {}

    return render(request, 'hobbiesApp/commonhobbies.html', context)


def search(request):

    context = {}

    return render(request, 'hobbiesApp/search.html', context)


@login_required(login_url='login')
def similarHobbies(request):

    # user currently logged in
    user = MyUser.objects.get(username=request.user)
    arr = []
    hobby = Hobby.objects.all()
    counting = MyUser.objects.all().count()
    for eachHobby in user.hobbies.all():
        for secondUser in MyUser.objects.all():
            if eachHobby in secondUser.hobbies.all():
                if secondUser != user:
                    arr.append(secondUser.username)
    x = Counter(arr).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))

    similar_hobbies.sort(key=lambda x: x[1], reverse=True)

    context = {'hobby': hobby, 'user': user, 'arr': arr,
               'test': test, 'similar_hobbies': similar_hobbies}

    return render(request, 'hobbiesApp/similarHobbies.html', context)


@login_required(login_url='login')
def similar_hobbies_api(request):
    user = MyUser.objects.get(
        username=request.user)  # user currently logged in
    users = []
    for eachHobby in user.hobbies.all():
        for secondUser in MyUser.objects.all():
            if eachHobby in secondUser.hobbies.all():
                if secondUser != user:
                    users.append(secondUser)
    x = Counter(users).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))
    similar_hobbies.sort(key=lambda x: x[1], reverse=True)

    return JsonResponse({
        'users': [user[0].to_dict() for user in similar_hobbies],
        'similar_hobbies': [hobby[1] for hobby in similar_hobbies],
    })


@login_required(login_url='login')
def filter_by_city(request):
    user = MyUser.objects.get(
        username=request.user)  # user currently logged in
    users = []
    for eachHobby in user.hobbies.all():
        for secondUser in MyUser.objects.all():
            if eachHobby in secondUser.hobbies.all():
                if secondUser != user:
                    users.append(secondUser)
    x = Counter(users).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))
    similar_hobbies.sort(key=lambda x: x[0].city, reverse=False)

    return JsonResponse({
        'users': [user[0].to_dict() for user in similar_hobbies],
        'similar_hobbies': [hobby[1] for hobby in similar_hobbies],
    })


@login_required(login_url='login')
def filter_by_username(request):
    user = MyUser.objects.get(
        username=request.user)  # user currently logged in
    users = []
    for eachHobby in user.hobbies.all():
        for secondUser in MyUser.objects.all():
            if eachHobby in secondUser.hobbies.all():
                if secondUser != user:
                    users.append(secondUser)
    x = Counter(users).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))
    similar_hobbies.sort(key=lambda x: x[0].username, reverse=False)

    return JsonResponse({
        'users': [user[0].to_dict() for user in similar_hobbies],
        'similar_hobbies': [hobby[1] for hobby in similar_hobbies],
    })


@login_required(login_url='login')
def filter_by_age(request):
    user = MyUser.objects.get(
        username=request.user)  # user currently logged in
    users = []
    for eachHobby in user.hobbies.all():
        for secondUser in MyUser.objects.all():
            if eachHobby in secondUser.hobbies.all():
                if secondUser != user:
                    users.append(secondUser)
    x = Counter(users).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))
    similar_hobbies.sort(
        key=lambda x: x[0].dob, reverse=False)

    return JsonResponse({
        'users': [user[0].to_dict() for user in similar_hobbies],
        'similar_hobbies': [hobby[1] for hobby in similar_hobbies],
    })


@login_required(login_url='login')
def search(request):
    user = MyUser.objects.get(
        username=request.user)  # user currently logged in
    users = []
    jsonbody = json.loads(request.body)
    city = jsonbody['city']
    minAge = age_to_dob(
        int(jsonbody['maxage'])) if jsonbody['maxage'] != '' else datetime.date(1500, 1, 1)
    maxAge = age_to_dob(
        int(jsonbody['minage'])) if jsonbody['minage'] != '' else datetime.date.today()
    for eachHobby in user.hobbies.all():
        if city != '':
            for secondUser in MyUser.objects.filter(city__contains=city, dob__lt=(maxAge), dob__gt=(minAge)):
                if eachHobby in secondUser.hobbies.all():
                    if secondUser != user:
                        users.append(secondUser)
        elif minAge != '' and maxAge != '':
            for secondUser in MyUser.objects.filter(dob__lt=(maxAge), dob__gt=(minAge)):
                if eachHobby in secondUser.hobbies.all():
                    if secondUser != user:
                        users.append(secondUser)
        else:
            for eachHobby in user.hobbies.all():
                for secondUser in MyUser.objects.all():
                    if eachHobby in secondUser.hobbies.all():
                        if secondUser != user:
                            users.append(secondUser)

    x = Counter(users).items()
    similar_hobbies = []
    for i in x:
        similar_hobbies.append((i[0], i[1]))
    similar_hobbies.sort(
        key=lambda x: x[1], reverse=True)
    print(similar_hobbies)

    return JsonResponse({
        'users': [user[0].to_dict() for user in similar_hobbies],
        'similar_hobbies': [hobby[1] for hobby in similar_hobbies],
    })


@login_required(login_url='login')
def age_to_dob(dob):
    return datetime.date.today() - datetime.timedelta(days=(dob*365)+365)
