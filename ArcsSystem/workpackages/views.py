from django.shortcuts import render
from django.views.generic import DetailView, ListView
from workpackages.models import WorkPackage, Theme

# Create your views here.


class WorkpackagesListView(ListView):
    ''''''
    model = WorkPackage
    template_name = 'workpackages/workpackages_list.html'


class WorkpackagesCategoryView(ListView):
    ''''''
    model = Theme
    template_name = 'workpackages/category_view.html'




class WorkpackagesDetailView(DetailView):
    ''''''
    model = Theme
    template_name = 'workpackages/theme_view.html'
