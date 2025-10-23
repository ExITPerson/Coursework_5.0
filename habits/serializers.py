from rest_framework import serializers

from habits.models import Award, Habit


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = ['id', 'title', 'description']

class HabitSerializer(serializers.ModelSerializer):
    award_habit = AwardSerializer(many=True, read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'title', 'author',
            'place', 'lead_time', 'action',
            'pleasant_habit', 'related_habit', 'period',
            'time_to_complete', 'public', 'award_habit'
        ]

    def validate(self, data):
        pleasant = data.get('pleasant_habit', False)
        instance = self.instance
        awards_exist = instance.award_habit.exests() if instance else False

        if pleasant and awards_exist:
            raise serializers.ValidationError('У приятной привычки не может быть привязанного вознаграждения')

        return data