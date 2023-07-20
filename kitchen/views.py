from django.shortcuts import render

from kitchen.models import Dish, Cook, DishType


def index(request):
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()
    num_dish_types = DishType.objects.count()

    context = {
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
    }

    return render(request, "kitchen/index.html", context=context)
