from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from kitchen.models import Cook, Dish, DishType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from kitchen.forms import CookSearchForm


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

    def get_queryset(self):
        self.search_form = CookSearchForm(self.request.GET or None)
        queryset = super().get_queryset()

        if self.search_form.is_valid():
            username = self.search_form.cleaned_data['username']
            min_experience = self.search_form.cleaned_data['min_experience']
            max_experience = self.search_form.cleaned_data['max_experience']

            if username:
                queryset = queryset.filter(username__icontains=username)
            if min_experience is not None:
                queryset = queryset.filter(
                    years_of_experience__gte=min_experience
                )
            if max_experience is not None:
                queryset = queryset.filter(
                    years_of_experience__lte=max_experience
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        return context


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
        'years_of_experience',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    template_name = 'kitchen/cook_form.html'
    success_url = reverse_lazy('kitchen:cook-list')


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = [
        'years_of_experience',
        'username',
        'email',
        'first_name',
        'last_name'
    ]
    template_name = 'kitchen/cook_form.html'
    success_url = reverse_lazy('kitchen:cook-list')


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = 'kitchen/cook_confirm_delete.html'
    success_url = reverse_lazy('kitchen:cook-list')


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = 'kitchen/cook_detail.html'
