from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("home/", views.home_view, name="home"),
    path("comments/<int:climb_id>/", views.comments_view, name="comments"),
    path("ascent/", views.AscentView.as_view(), name="ascent"),
    path("logbook/", views.logbook_view, name="logbook"),
    path("logbookUpdate/<int:ascent_id>", views.LogbookUpdateView.as_view(), name="logbookUpdate"),
    path("logbookDelete/<int:ascent_id>", views.LogbookDeleteView.as_view(), name="logbookDelete"),
]