from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import FeedbackForm


# Create your views here.
def home(request):
    return render(request, "home.html", {})


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # TODO: Save the feedback to the database
            # For right now just prints the feedback to the console
            print(form.cleaned_data["feedback"])
            return redirect("home")
    else:
        form = FeedbackForm()
    return redirect("home")
