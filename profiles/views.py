from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .form import ProfileForm
from .models import Profile

@login_required
def profile_view(request):
    # Try to get the user's profile; create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            form.save()  # Save the updated profile
            return redirect('profiles:profile_view')  # Redirect after saving
    else:
        form = ProfileForm(instance=profile)  # Prepopulate the form with user's profile data

    return render(request, 'profile/profiles.html', {'form': form, 'user': request.user})
# Render the profile template
  # Render the profile template

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('profiles:profile_view')  # Redirect to a profile view
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'form': form})