from django.urls import path

from .views import WeeklyMenuView


urlpatterns = [
    path("mess/menu", WeeklyMenuView.as_view(), name="weekly-mess-menu"),
]
