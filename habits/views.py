from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Award, Habit
from habits.paginators import HabitAndAwardPaginator
from habits.permissions import AuthorPermission
from habits.serializers import HabitSerializer, AwardSerializer, HabitPublicSerializer


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = HabitAndAwardPaginator

    @swagger_auto_schema(request_body=AwardSerializer,)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            habit_id = request.data.get('habit')
            if habit_id is None:
                return Response({'habit': 'Это поле обязательно.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(author=request.user, habit_id=habit_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, AuthorPermission]

        return [permission() for permission in self.permission_classes]


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.filter(pleasant_habit=False)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, AuthorPermission]
    pagination_class = HabitAndAwardPaginator

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(author=user)


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, AuthorPermission]


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, AuthorPermission]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, AuthorPermission]


class HabitPublicListAPIView(generics.ListAPIView):
    queryset = Habit.objects.filter(public=True, pleasant_habit=False)
    serializer_class = HabitPublicSerializer
    permission_classes = [IsAuthenticated, AuthorPermission]
    pagination_class = HabitAndAwardPaginator
