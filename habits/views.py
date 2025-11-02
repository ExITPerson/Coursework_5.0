from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from habits.models import Award, Habit
from habits.serializers import HabitSerializer, AwardSerializer


class AwardViewSet(viewsets.ViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            habit_id = request.data.get('habit')
            if habit_id is None:
                return Response({'habit': 'Это поле обязательно.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(author=request.user, habit_id=habit_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.filter(pleasant_habit=False)
    serializer_class = HabitSerializer


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()