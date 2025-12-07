from rest_framework.routers import DefaultRouter
from django.urls import path

from habits.apps import HabitsConfig
from habits.views import AwardViewSet, HabitListAPIView, HabitCreateAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    HabitRetrieveAPIView, HabitPublicListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'award', AwardViewSet, basename='award')

urlpatterns = [
    path('public_habit/', HabitPublicListAPIView.as_view(), name='public_habit_list'),
    path('habit/', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/create/', HabitCreateAPIView.as_view(), name='create_habit'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='detaild_habit'),
    path('habit/<int:pk>/update/', HabitUpdateAPIView.as_view(), name='update_habit'),
    path('habit/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='delete_habit'),
] + router.urls
