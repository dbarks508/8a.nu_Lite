from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from .models import Climb, Ascent
from .forms import AscentForm
import re

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # make sure you have a 'login' URL name
    else:
        form = UserCreationForm()
    
    return render(request, "logbookApp/register.html", {"form": form})

# classic log in view 
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    return render(request, "logbookApp/login.html", {"form": form})

# shows all available climbs to log
def home_view(request):
    climbs_lcc = Climb.objects.filter(area="lcc").annotate(grade_num=Cast(Substr("grade", 2), IntegerField())).order_by("grade_num")
    climbs_o = Climb.objects.filter(area="o").annotate(grade_num=Cast(Substr("grade", 2), IntegerField())).order_by("grade_num")
    context = {"climbs_lcc": climbs_lcc, "climbs_o": climbs_o, "user": request.user}
    return render(request, "logbookApp/home.html", context)

# form view to log an ascent of a climb - takes climb name from request to display
class AscentView(FormView):
    template_name = "logbookApp/ascent.html"
    form_class = AscentForm
    success_url = "/logbook/"
    
    # used to pre populate the update form with current ascent data
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ascent_id = self.kwargs.get("ascent_id")
        if ascent_id:
            ascent = get_object_or_404(Ascent, id=self.kwargs["ascent_id"], user=self.request.user)
            kwargs["instance"] = ascent
        return kwargs

    def form_valid(self, form):
        ascent = form.save(commit=False)
        ascent.user = self.request.user
        
        # make sure the grade input is proceeded by v
        proposedGrade = form.cleaned_data.get("proposedGrade")
        result = re.match(r'^[Vv]\d+$', proposedGrade)
        if not result:
            form.add_error("proposedGrade", "grade must start with v")
            return self.form_invalid(form)
        
        # grab the passed in climb
        climb_id = self.request.GET.get("climb_id")
        if climb_id:
            ascent.climb = get_object_or_404(Climb, id=climb_id)
        
        ascent.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # get ascent info if availaible
        ascent_id = self.kwargs.get("ascent_id")
        if ascent_id:
            ascent = get_object_or_404(Ascent, id=self.kwargs["ascent_id"], user=self.request.user)
            context["ascent"] = ascent
        
        # get climb info if available
        climb_id = self.request.GET.get("climb_id")
        if climb_id:
            context["climb"] = get_object_or_404(Climb, id=climb_id)
        return context
            
# pass all the ascents of the loggin in user 
def logbook_view(request):
    loggedAscents = Ascent.objects.filter(user=request.user).order_by('-date')
    context = {"loggedAscents": loggedAscents}
    return render(request, "logbookApp/logbook.html", context)

# filter climb and climb comments from the passed in id via url
def comments_view(request, climb_id):
    climb = Climb.objects.get(id=climb_id)
    comments = Ascent.objects.filter(climb_id=climb_id).exclude(comment="")
    context = {"climb": climb, "comments": comments}
    
    return render(request, "logbookApp/comments.html", context)
    

# update existing Ascent view class
class LogbookUpdateView(AscentView):
    model = Ascent
    template_name = "logbookApp/logbookUpdate.html"
    form_class = AscentForm
    success_url = "/logbook/"

# delete existing pi view class
class LogbookDeleteView(AscentView):
    model = Ascent
    template_name = "logbookApp/logbookDelete.html"
    success_url = "/logbook/"