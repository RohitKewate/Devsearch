from . import views
from django.urls import path



urlpatterns = [
    path('', views.profiles, name='profile-page'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile-page'),
    path('login/', views.loginUser, name='login-page'),
    path('logout/', views.logoutUser, name='logout-page'),
    path('register/', views.registerUser, name='register-page'),
    path('account/', views.userAccount, name='user-account-page'),
    path('edit-account/', views.editAccount, name='edit-account-page'),
    path('add-skill/', views.addSkills, name='add-skill-page'),
    path('edit-skill/<str:pk>/', views.updateSkills, name='edit-skill-page'),
    path("delete-skill/<str:pk>/", views.deleteSkill, name="delete-skill-page"),
    path("inbox/", views.inbox, name="inbox-page"),
    path("message/<str:pk>/", views.viewMessage, name="message-page"),
    path("send-message/<str:pk>/", views.createMessage, name="send-message-page"),
    path("contact-us/", views.contactUs, name="contact-us-page"),
    path("thank-you/", views.thankYou, name="thank-you-page"),
]