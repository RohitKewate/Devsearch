from . import views
from django.urls import path


urlpatterns = [
    path("", views.home, name="home-page"),
    path("projects/", views.projects, name="projects-page"),
    path("projects/<str:pk>/", views.project, name="single-project-page"),
    path("create-project/", views.createProject, name="create-project-page"),
    path("update-project/<str:pk>/", views.updateProject, name="update-project-page"),
    path("delete-project/<str:pk>/", views.deleteProject, name="delete-project-page"),
]
