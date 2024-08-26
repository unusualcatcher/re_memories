import os
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from memories.models import Memory
from chat.models import ChatGroup
from django.contrib import messages
from .models import Profile
import random
import string

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('password2')
            username_exists = User.objects.filter(username=username).first()
            email_exists = User.objects.filter(email=email).first()
            if username_exists:
                return render(request, 'users/register.html', {'username_error':'That username is already taken. Please choose a different one.'})
            if email_exists:
                return render(request, 'users/register.html', {'email_error':'That email is already registered with an account.'})
            if password == confirm_password:
                hashed_password = make_password(password)
                user = User.objects.create(username=username, email=email, password=hashed_password)
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                return render(request, 'users/register.html', {'success_message':'Registered successfully. You can now log in!'})
            else:
                return render(request, 'users/register.html', {'password_error':'Please ensure that the password and confirm password fields are equal.'})
        return render(request, 'users/register.html',)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'users/login.html', {'error_message': 'Invalid username or password.'})
        return render(request, 'users/login.html')


@login_required
def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        memories = Memory.objects.filter(author=profile.user)
        return render(request, 'users/profile.html', {'profile':profile, 'user':request.user,
                                                      'memories':memories})
    else:
        return redirect('register')

def generate_random_string(length=10):
    """Generate a random string of numbers with the specified length."""
    return ''.join(random.choices(string.digits, k=length))

@login_required
def update_user_info(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profile_pic = request.FILES.get('profilePic')
        user = request.user
        if username:
            username_exists = User.objects.filter(username=username).first()
            if username_exists:
                if request.user.username != username:
                    
                    return render(request, 'users/update_profile.html', {'error_message':'That username is already taken. Please choose a different one.'})
            user.username = username

        if profile_pic:
            profile, created = Profile.objects.get_or_create(user=user)
            base, ext = os.path.splitext(profile_pic.name)
            new_filename = f"{generate_random_string()}{ext}"
           
            profile.pfp.save(new_filename, profile_pic, save=False)
            profile.save()  

        user.save()  

        return redirect('profile')  

    else:
        # GET request, render the form
        profile, created = Profile.objects.get_or_create(user=request.user)
        context = {
            'profile': profile,
        }
        return render(request, 'users/update_profile.html', context)
    
@login_required
def view_profile(request, username):

    user = User.objects.filter(username=username).first()
    profile = Profile.objects.filter(user=user).first()
    is_own_profile = request.user == profile.user
    memories = Memory.objects.filter(author=profile.user)
    
    if request.method == 'POST':

        chat_exists = ChatGroup.objects.filter(
            member1=request.user, member2=profile.user
        ).exists() or ChatGroup.objects.filter(
            member1=profile.user, member2=request.user
        ).exists()
        
        if chat_exists:
       
            existing_chat = ChatGroup.objects.filter(
                member1=request.user, member2=profile.user
            ).first() or ChatGroup.objects.filter(
                member1=profile.user, member2=request.user
            ).first()
            
           
            return redirect('chatroom', group_name=existing_chat.group_name)
        elif not is_own_profile:
            
            random_name = random_string()
            ChatGroup.objects.create(
                group_name=random_name,
                member1=request.user,
                member2=profile.user
            )
            return redirect('chatroom', group_name=random_name)
    
    return render(request, 'users/view_profile.html', {
        'profile': profile,
        'memories': memories,
        'is_own_profile': is_own_profile
    })