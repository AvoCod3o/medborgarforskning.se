from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomUserPrivateForm
from django import forms
from staticpages.models import TermsPage
from django.contrib.auth import logout
from datetime import date

from django import forms

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from projects.models import ProjectSubmission, ProjectEntry, KeywordSwe, KeywordEng, KeywordLine

class UserPublicProfilePageView(DetailView):
    template_name = 'users/public_profile_view.html'

    def get_object(self, queryset=None):
        obj = None
        if "username" in self.kwargs.keys():
            try:
                obj = CustomUser.objects.get(username=self.kwargs['username'])
                print(obj)
            except ObjectDoesNotExist:
                pass
        else:
            if self.request.user.is_authenticated:
                obj = self.request.user
            else:
                pass
        print(obj)
        # if obj is None:
        #     raise Http404()
        return obj

def UserPrivateProfilePageView(request):

    template_name = 'users/private_profile_view.html'
    context = {}

    # new page : get page
    if request.method == "GET":
        # admin part
        if request.user.is_superuser:
            context["Admin_project_submissions"] = ProjectSubmission.objects.all()
            # all users 
        if request.user.is_authenticated:
            context["My_approved_projects"] = ProjectEntry.objects.filter(created_by = request.user)
            context["My_pending_projects"] =  ProjectSubmission.objects.filter(created_by = request.user)

        return render(request, template_name, context)

    # this is the admin accept sub-forms part
    if request.method == "POST":
        #check if admin
        if request.user.is_superuser:
            for name in request.POST:
                if "acpt_" in name:
                    accept_subForm(name[5:])
        return HttpResponseRedirect(reverse('userprofile_private_view'))






# this funtion create projectEntry from projectSub 
# and handels keyword submitions
# alsow creating keyword line
def accept_subForm(id):

    sub_model = ProjectSubmission.objects.get(id = int(id))

    pro_kwargs = sub_model.__dict__.copy()
    if "_state" in pro_kwargs:
        del pro_kwargs["_state"]
    if "id" in pro_kwargs:
        del pro_kwargs["id"]
    if "keywords_sv" in pro_kwargs:
        del pro_kwargs["keywords_sv"]
    if "keywords_en" in pro_kwargs:
        del pro_kwargs["keywords_en"]

    new_model = ProjectEntry(**pro_kwargs)
    new_model.save()


    for key_sv, key_en in zip(*sub_model.get_keywords()):


        # if both are empty continue 
        if key_sv == "" and key_en == "":
            continue

        # if sv is empty but not en
        if key_sv == "":

            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()
            options = model_keyword_eng.line.filter(swe=None)

            if len(options) > 0:
                new_model.add_keyword(options.first())

            else:
                model_keyword_line =  KeywordLine(eng=model_keyword_eng)
                model_keyword_line.save()
                new_model.add_keyword(model_keyword_line)


        # if sv is empty but not en
        elif key_en == "":

            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()
            options = model_keyword_swe.line.filter(eng=None)

            if len(options) > 0:
                new_model.add_keyword(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe)
                model_keyword_line.save()
                new_model.add_keyword(model_keyword_line)

        # both are filed-in        
        else:

            # en key
            matching_keywords_en = KeywordEng.objects.filter(keyword=key_en.lower())
            if len(matching_keywords_en) > 0:
                model_keyword_eng = matching_keywords_en.first()

            else:
                model_keyword_eng = KeywordEng(keyword =  key_en.lower())
                model_keyword_eng.save()


            # sv key
            matching_keywords_sv = KeywordSwe.objects.filter(keyword=key_sv.lower())
            if len(matching_keywords_sv) > 0:
                model_keyword_swe = matching_keywords_sv.first()

            else:
                model_keyword_swe = KeywordSwe(keyword =  key_sv.lower())
                model_keyword_swe.save()


            options = model_keyword_swe.line.filter(eng=model_keyword_eng)

            if len(options) > 0:
                new_model.add_keyword(options.first())

            else:
                model_keyword_line =  KeywordLine(swe=model_keyword_swe, eng=model_keyword_eng)
                model_keyword_line.save()
                new_model.add_keyword(model_keyword_line)

    new_model.save()
    sub_model.delete()



class UserEidtMyPageView(TemplateView):

    template_name = "users/profile_edit_view.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CustomUserPrivateForm(initial={

                'username': request.user.username, 
                'email': request.user.email,
                'title': request.user.title,
                'bio_general': request.user.bio_general,
                'bio_research_interest': request.user.bio_research_interest,
                'personal_website_address': request.user.personal_website_address,
                'institution': request.user.institution,
                "first_name":  request.user.first_name, 
                "last_name": request.user.last_name,

                  })
            for key, value in form.fields.items():
                value.disabled = True
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('account_login'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CustomUserPrivateForm(request.POST)
            print(form.errors.as_data())

            if form.is_valid() :
                request.user.email = form["email"].value()
                request.user.title = form["title"].value()
                request.user.bio_general = form["bio_general"].value()
                request.user.bio_research_interest = form["bio_research_interest"].value()
                # request.user.connections = form["connections"].value()
                # request.user.institution = form["institution"].value()
                request.user.personal_website_address = form["personal_website_address"].value()
                request.user.institution = form["institution"].value()
                request.user.first_name = form["first_name"].value()
                request.user.last_name = form["last_name"].value()
                request.user.save()
                return redirect("userprofile_private_view")
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect(reverse('account_login'))


class AcceptTermsPageView(TemplateView):

    template_name = "users/accept_terms_view.html"

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            latest_term = TermsPage.objects.latest('version_number')
            if request.user.accepted_eula_version == latest_term.version_number:
                return redirect("staticpages:homepage_view")
            else:
                return render(request, self.template_name, {'term_object': latest_term})
        else:
            return HttpResponseRedirect(reverse('account_login'))

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            acceptFlag = (request.POST.get("accept", "") == 'true');
            if acceptFlag:
                request.user.accepted_eula = True
                request.user.accepted_eula_version = request.POST.get("term-version", "")
                request.user.accepted_eula_date = date.today()
                request.user.save()
            else:
                logout(request)
            return redirect("staticpages:homepage_view")
        else:
            return HttpResponseRedirect(reverse('account_login'))
