from django.shortcuts import render
from kitchen.models import Cook, Dish, DishType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    avaible_cooks = Cook.objects.count()

    context = {
        'avaible_cooks': avaible_cooks,
    }

    return render(request, 'index.html', context=context)
