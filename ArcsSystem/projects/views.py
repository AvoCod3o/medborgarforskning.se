from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from projects.models import Project

'''
# Quick Fuction based template
def template_view(request):
'''
'''
    context = {
        }
    return render(request, 'exampletemplate.html', context)
'''

# Create your views here.

class ProjectListView(ListView):
    '''
    '''
    model = Project
    template_name = 'projects/project_list.html'
#def project_list_view(request):
#    project_list = Project.objects.all()
#    context = {
#        'project_list' : project_list,
#    }
#    return render(request, 'project_list.html', context)


class ProjectDetailView(DetailView):
    '''
    '''
    model = Project
    template_name = 'projects/project_detail.html'