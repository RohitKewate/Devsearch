from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.conf import settings
from .models import profile, User, Message
from .utils import searchProfile, paginateProfiles, sendWelcomeEmailToClient, contactUs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def loginUser(request):
    page = 'login-page'
    if request.user.is_authenticated:
        return redirect("profile-page")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = profile.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-account-page')
        else:
            messages.error(request, "Invalid Credentials")

    context = {'page': page}
    return render(request, 'users/login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login-page")


def registerUser(request):
    page = 'registration-page'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            sendWelcomeEmailToClient(user)
            user = form.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-account-page')
        else:
            messages.error(request, "Something went wrong!")

    context = {'page': page, 'form': form}
    return render(request, 'users/login_registration.html', context)


def userProfile(request, pk):
    userProfile = profile.objects.get(id=pk)

    topSkills = userProfile.skill_set.exclude(description__exact=" ")
    otherSkills = userProfile.skill_set.filter(description="")
    context = {'user': userProfile,
               'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user_profile.html', context)


def profiles(request):
    profiles, search_query = searchProfile(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


@login_required(login_url="login-page")
def userAccount(request):
    profile = request.user.profile
    Skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': Skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url="login-page")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-account-page')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login-page")
def addSkills(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill Added')
            return redirect('user-account-page')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login-page")
def updateSkills(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill Updated')
            return redirect('user-account-page')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login-page")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill Deleted')
        return redirect('user-account-page')
    context = {'object': skill}
    return render(request, 'users/delete_template.html', context)


@login_required(login_url="login-page")
def inbox(request):
    profile = request.user.profile
    recepientMessages = profile.messages.all()
    unreadCount = recepientMessages.filter(is_read=False).count()

    context = {'recepientMessages': recepientMessages,
               'unreadCount': unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login-page")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    recipient = profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was sucessfully sent!")
            return redirect("user-profile-page", pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, "users/message_form.html", context)


def contactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        newSubject = "From "+name+": "+subject
        send_mail(
            newSubject,
            message,
            email,
            [settings.EMAIL_HOST_USER],
        )
        return redirect('thank-you-page')

    return render(request, "users/contact.html", )


def thankYou(request):
    return render(request, "users/thankyou.html")
