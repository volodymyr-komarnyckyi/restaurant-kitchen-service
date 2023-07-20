from django.http import Http404
from django.shortcuts import render
from django.views import generic

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


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")


class DishDetailView(generic.DetailView):
    model = Dish

# def dish_detail_view(request, pk):
#     try:
#         dish = Dish.objects.get(pk=pk)
#     except Dish.DoesNotExist:
#         raise Http404("Book does not exist!")
#
#     context = {
#         "dish": dish,
#     }
#
#     return render(request, "kitchen/dish_detail.html", context=context)


class CookListView(generic.ListView):
    model = Cook
