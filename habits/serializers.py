from rest_framework import serializers

from habits.models import Award, Habit


class AwardSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all())

    class Meta:
        model = Award
        fields = ['id', 'title', 'description', 'author', 'habit']

    def validate(self, data):
        habit = data.get('habit')
        if not habit:
            raise serializers.ValidationError("Связанная привычка обязательна.")

        # Проверка, что привычка не является приятной
        if habit.pleasant_habit:
            raise serializers.ValidationError("Нельзя создавать вознаграждение для приятной привычки.")

        # Проверка что у привычки нет связанных приятных привычек
        related_pleasant_habits = habit.related_to.filter(pleasant_habit=True)
        if related_pleasant_habits.exists():
            raise serializers.ValidationError(
                "У привычки с привязанной приятной привычкой нельзя создавать вознаграждение.")

        return data


class HabitSerializer(serializers.ModelSerializer):
    award_habit = AwardSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id')
    list_of_pleasant_habits = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'author',
            'place', 'lead_time', 'action',
            'pleasant_habit', 'related_habit', 'period',
            'time_to_complete', 'public', 'award_habit',
            'list_of_pleasant_habits'
        ]

    def get_list_of_pleasant_habits(self, obj):
        pleasant_habits = obj.related_to.filter(pleasant_habit=True)
        return HabitSerializer(pleasant_habits, many=True, context=self.context).data

    def validate(self, data):
        pleasant_habit = data.get('pleasant_habit', getattr(self.instance, 'pleasant_habit', False))
        related_habit = data.get('related_habit', getattr(self.instance, 'related_habit', None))
        instance = self.instance

        # Существующие награды у текущей привычки (если обновление)
        awards_exist = instance.award_habit.exists() if instance else False

        if pleasant_habit:
            # Для приятной привычки related_habit обязателен
            if related_habit is None:
                raise serializers.ValidationError('Приятная привычка должна быть связана с обычной привычкой.')

            if related_habit.pleasant_habit:
                raise serializers.ValidationError(
                    'Приятная привычка не может быть связана с другой приятной привычкой.')

            # Новая проверка: у связанной обычной привычки не должно быть наград
            if related_habit.award_habit.exists():
                raise serializers.ValidationError(
                    'Привязанная обычная привычка уже имеет награды, к ней нельзя привязать приятную привычку.'
                )

            if awards_exist:
                raise serializers.ValidationError('К приятной привычке нельзя привязывать вознаграждения.')

        else:
            # Для обычной привычки related_habit всегда None
            if related_habit is not None:
                raise serializers.ValidationError('Обычная привычка не должна быть связана с другой привычкой.')

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    award_habit = AwardSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.id')
    list_of_pleasant_habits = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'author',
            'place', 'lead_time', 'action',
            'pleasant_habit', 'related_habit', 'period',
            'time_to_complete', 'public', 'award_habit',
            'list_of_pleasant_habits'
        ]

    def get_list_of_pleasant_habits(self, obj):
        pleasant_habits = obj.related_to.filter(pleasant_habit=True, public=True)
        return HabitSerializer(pleasant_habits, many=True, context=self.context).data
