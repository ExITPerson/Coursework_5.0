from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class CategoryHabit(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
