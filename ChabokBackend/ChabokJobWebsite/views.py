from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .forms import CreateUserForm
from .serializers import jobSeekerHomePageSerializer
from .usecases import *


def sign_up(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Acount created successfuly")
            return redirect('login')
    context = {'form': form}
    return render(request, 'signup.html', context)


def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')


def home_page(request):
    context = {}
    if request.method == "GET":
        user = request.user
        try:
            if user.get_role() == "EMPLOYER":
                job_offers = find_jobOffers_by_user(user)
                context = {
                    "job_offers": jobOfferSerializer(job_offers, many=True).data
                }
                return render(request, 'viewjobs.html', context)
            else:
                context = jobSeekerHomePageSerializer(user).data
                return render(request, 'main.html', context)
        except:
            return redirect('login')
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


def view_job(request, pk):
    context = {}
    user = request.user
    job_offer = get_jobOffer_by_id(pk)
    context = jobOfferSerializer(job_offer).data
    try:
        if user.get_role() == "EMPLOYER":
            context["applications"] = viewJobApplicantsSerializer(job_offer).data
            return render(request, 'viewjobapplicants.html', context)
        else:
            if request.method == "POST":
                application = create_application(user, job_offer)
                return redirect('viewjob', pk=pk)
            return render(request, 'singlejob.html', context)
    except:
        return render(request, 'singlejob.html', context)


def create_job(request):
    context = {}
    user = request.user
    # try:
    if user.get_role() == "EMPLOYER":
        if request.method == "POST":
            job_offer = jobOfferSerializer(request.POST)
            jobOffer = create_job_offer(job_offer.data, user)
            return redirect('viewjob', pk=jobOffer.id)
        return render(request, 'addjob.html', context)
    # except:
    #     pass
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    


def delete_job(request, pk):
    user = request.user
    job_offer = get_jobOffer_by_id(pk)
    if job_offer.author.id == user.id:
        delete_job_offer(job_offer)
        return redirect('viewjoblist')
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)


def edit_job(request, pk):
    user = request.user
    job_offer = get_jobOffer_by_id(pk)
    if job_offer.author.id == user.id:
        context = jobOfferSerializer(job_offer).data
        if request.method == "POST":
            jobOffer = editJobOfferSerializer(request.POST)
            if jobOffer.is_valid(raise_exception=True):
                job_offer = update_job_offer(job_offer, jobOffer.validated_data)
                return redirect('viewjob', pk=job_offer.id)
        return render(request, 'addjob.html', context)
    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    

def profile(request):
    user = request.user
    if user is not None:
        context = userProfileSerializer(user).data
        if request.method == "POST":
            user_profile = editUserProfileSerializer(request.POST)
            request.user = update_user_profile(user, user_profile.data)
            messages.success(request, "Profile updated successfuly")
            return redirect('profile')
        return render(request, 'profile.html', context)
    return redirect('login')