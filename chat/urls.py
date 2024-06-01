from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),
    path('<str:room_slug>/', views.room, name="room"),
]