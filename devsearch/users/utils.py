from django.db.models import Q
from .models import profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings


def sendWelcomeEmailToClient(user):
    send_mail(
        "Welcome To Devsearch",
        "We are glad to welcome you to our community",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


def contactUs(name, email, subject, message):
    newSubject = "From "+name+": "+subject
    send_mail(
        newSubject,
        message,
        email,
        [settings.EMAIL_HOST_USER],
    )
    return name, email, subject, message


def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfile(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)

    )
    return profiles, search_query
