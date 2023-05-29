from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm, ProfileForm, PostForm
from .models import Profile, Post, Comment

import json, datetime


def login_action(request):
    context = {}
    context['page_name'] = 'Login'
    form = LoginForm(request.POST)
    context['form'] = form

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return redirect(reverse('global'))
    else:
        context['form'] = LoginForm()
        return render(request, 'login.html', context)


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))
    

def register(request):

    context = {}
    context['page_name'] = "Register"
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                first_name = form.cleaned_data['first_name'],
                                                last_name = form.cleaned_data['last_name'],
                                                email = form.cleaned_data['email'],
                                                password = form.cleaned_data['password'],
                                                )
            new_user.save()

            new_user = authenticate(username = form.cleaned_data['username'],
                                    password = form.cleaned_data['password'])

            new_profile = Profile(user=new_user)
            new_profile.save()
            new_user.profile = new_profile
         
            return redirect(reverse('login'))
    
    else:
        context['form'] = RegisterForm()

    return render(request, "register.html", context)


@login_required(login_url='login')
def globalStream(request):
    
    context = {}
    context['page_name'] = 'Global Stream'
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name

    # # renders the other posts
    # if request.method == 'GET':
    #     context['posts'] = Post.objects.all().order_by('-date')
    #     context['form'] = PostForm()

    #     return render(request, 'global.html', context)

    # if 'post_input_text' not in request.POST or not request.POST['post_input_text']:
    #     context['posts'] = Post.objects.all().order_by('-date')
    #     context['form'] = PostForm()

    #     return render(request, 'global.html', context)

    
    # new_form = PostForm(request.POST)
    # context['form'] = new_form
    
    # if new_form.is_valid():

    #     new_post = Post(new_post=new_form.cleaned_data['post_input_text'], user=request.user, date = timezone.now())
    #     new_post.save()

    # context['posts'] = Post.objects.all().order_by('-date')

    return render(request, 'global.html', context)

# Getting response in json format
def globalStream_json_serializer(request):
    response_data = {'posts':[], 'comments':[]}

    for model_item in Post.objects.all():

        my_item = {
            'id': model_item.id,
            'pk': model_item.pk,
            'new_post': model_item.new_post,
            'user_first_name': model_item.user.first_name,
            'user_last_name': model_item.user.last_name,
            'date': (model_item.date - datetime.timedelta(1)).strftime("%-m/%-d/%Y %-I:%M %p"),
            'user_id': model_item.user.id
        }
        response_data['posts'].append(my_item)
    
    # same thing for commeents
    for comment_item in Comment.objects.all():
        new_comment = {
            'id': comment_item.id,
            'new_comment': comment_item.text,
            'date': (comment_item.date - datetime.timedelta(1)).strftime("%-m/%-d/%Y %-I:%M %p"),
            'user_first_name': comment_item.user.first_name,
            'user_last_name': comment_item.user.last_name,
            'user_id': comment_item.user.id,
            'post_number': comment_item.post.id
        }
        response_data['comments'].append(new_comment)

    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')

def followerStream_json_serializer(request):
    response_data = {'posts':[], 'comments':[]}
    setOfFollowedUsers = set()

    for followUser in request.user.profile.following.all():
        setOfFollowedUsers.add(followUser.id)

    for model_item in Post.objects.all():

        if model_item.user.id in setOfFollowedUsers:
            print(f'this post {model_item} is valid')
            my_item = {
                'id': model_item.id,
                'pk': model_item.pk,
                'new_post': model_item.new_post,
                'user_first_name': model_item.user.first_name,
                'user_last_name': model_item.user.last_name,
                'date': (model_item.date - datetime.timedelta(1)).strftime("%-m/%-d/%Y %-I:%M %p"),
                'user_id':model_item.user.id
            }
            response_data['posts'].append(my_item)
        else:
            print(f'this post {model_item} is NOT valid')

    # for comments
    for comment_item in Comment.objects.all():
        if comment_item.post.user.id in setOfFollowedUsers:
            new_comment = {
                'id': comment_item.id,
                'new_comment': comment_item.text,
                'date': (comment_item.date - datetime.timedelta(1)).strftime("%-m/%-d/%Y %-I:%M %p"),
                'user_first_name': comment_item.user.first_name,
                'user_last_name': comment_item.user.last_name,
                'user_id': comment_item.user.profile.user_id,
                'post_number': comment_item.post.id,
            }
            response_data['comments'].append(new_comment)

   
    print(f'response data looks like {response_data}')
    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')


def add_comment(request):
    print("Python in the add_comment function")

    if request.method != "POST":
        return _my_json_error_response("You must have a POST request for this operation", status = 405)

    if not "item" in request.POST or not request.POST['item']:
        return _my_json_error_response("Ypu must ever a comment to add.", status = 400)

    post_id = request.POST['hiddenPostValue']
    parentPOST = get_object_or_404(Post, id=post_id)

    # Saving it to the database
    new_comment = Comment(text=request.POST['item'], user=request.user, date = timezone.now(), post=parentPOST)
    new_comment.save()

    pageToReturn = request.POST['page']

    if pageToReturn == '1':
        return globalStream_json_serializer(request)
    else:
        return followerStream_json_serializer(request)
        
@login_required(login_url='login')
def followerStream(request):
    
    context = {}
    context['page_name'] = 'Follower Stream'
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name

    # following = request.user.profile.following.values()
    # id_list = []
    # for v in following:
    #     id_list.append(v['id'])
    
    # context['posts']= Post.objects.filter(user_id__in=id_list).order_by('-date')

    return render(request, 'followers.html', context)


@login_required(login_url='login')
def myProfile(request, id):
    
    context = {}
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    user = get_object_or_404(User, id=id)

    userProfile = user.profile
    context['profile'] = userProfile

    if request.method == 'GET':
        context['form'] = ProfileForm(initial={'bio':userProfile.bio}) if userProfile.bio else ProfileForm()
        return render(request, 'myProfile.html', context)

    new_form = ProfileForm(request.POST, request.FILES)
    context['form'] = new_form

    if new_form.is_valid():
        newPicture = new_form.cleaned_data['profile_picture']

        if new_form.cleaned_data['profile_picture']:
            userProfile.profile_picture = new_form.cleaned_data['profile_picture']
            userProfile.content_type = new_form.cleaned_data['profile_picture'].content_type
        
        if new_form.cleaned_data['bio']:
            userProfile.bio = new_form.cleaned_data['bio']

        userProfile.save()

        context['profile'] = userProfile
        
        return render(request, 'myProfile.html', context)

    else:

        return render(request, 'myProfile.html', context)


@login_required(login_url='login')
def otherProfile(request, id):
    
    context = {}
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name
    user = get_object_or_404(User, id=id)
    
    userProfile = user.profile
    context['profile'] = userProfile

    if request.user.profile.following.filter(id=id).exists():
        context['button_name'] = "Unfollow"
    elif request.user.id == id:
        return render(request, "otherProfile.html", context) # user is looking at their own profile
    else:
        context['button_name'] = "Follow"

    if request.user.id == id:
        return render(request, 'otherProfile.html', context)
    elif request.user.profile.following.filter(id=id).exists():
        context['button_name'] = 'Unfollow'
    else:
        context['button_name'] = 'Follow'

    return render(request, 'otherProfile.html', context)


@login_required(login_url='login')
def follow(request, id):
    print('following function')
    context = {}
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name

    user_to_follow = get_object_or_404(User, id=id)
 
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()

    context['profile'] = user_to_follow.profile
    context['button_name'] = 'Unfollow'

    return render(request, 'otherProfile.html', context)


@login_required(login_url='login')
def unfollow(request, id):
    print('Unfollowing function')
    context = {}
    context['first_name'] = request.user.first_name
    context['last_name'] = request.user.last_name

    user_to_unfollow = get_object_or_404(User, id=id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()

    context['profile'] = user_to_unfollow.profile
    context['button_name'] = 'Follow'

    return render(request, 'otherProfile.html', context)


@login_required
def get_photo(request, id):
    
    item = get_object_or_404(Profile, user_id=id)

    if not item.profile_picture:
        raise Http404

    return HttpResponse(item.profile_picture, content_type=item.content_type)








    


