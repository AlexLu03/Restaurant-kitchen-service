from django.shortcuts import render
from django.views import generic
from kitchen.models import Cook, Dish, DishType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    avaible_cooks = Cook.objects.count()

    context = {
        'avaible_cooks': avaible_cooks,
    }

    return render(request, 'kitchen/index.html', context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    context_object_name = 'cook_list'
    template_name = 'kitchen/cook_list.html'
    paginate_by = 3


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = 'dish_list'
    template_name = 'kitchen/dish_list.html'
    paginate_by = 10


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = 'dishtype_list'
    template_name = 'kitchen/dishtype_list.html'
    paginate_by = 5


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = [
        'year_of_experience',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    template_name = 'kitchen/cook_form.html'
    success_url = '/kitchen/cooks/'
