from rest_framework.decorators import api_view
from rest_framework.response import Response
from habits.models import Habit
from.serializers import HabitSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/habits',
        'Get /api/habits/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getHabits(requet):
    habits = Habit.objects.all()
    serializer = HabitSerializer(habits, many=True)
    return Response(serializer.data)