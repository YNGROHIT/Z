from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.views.decorators.csrf import csrf_protect

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='signin')
def setting(request):
    # Get the user's profile
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist. Please contact support.")
        return redirect('setting')

    if request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        # Handle image upload
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            user_profile.profileimg = image
        else:
            # Keep the existing profile image if no new image is uploaded
            user_profile.profileimg = user_profile.profileimg

        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        messages.success(request, "Settings updated successfully.")
        return redirect('setting')
    print("-------------------------here---------------------------")
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')  # Fixed typo ('emial' -> 'email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken.')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken.')
                return redirect('signup')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Authenticate and create a profile for the user
                user_login = auth.authenticate(username=username, password=password)
                if user_login:
                    auth.login(request, user_login)
                
                new_profile = Profile.objects.create(user=user, id_user=user.id)
                new_profile.save()

                messages.success(request, 'User created successfully.')
                return redirect('signin')  # Redirect to the login page after signup
        else:
            messages.info(request, 'Passwords do not match.')
            return redirect('signup')
    else: 
        return render(request, 'signup.html')

@csrf_protect
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')
