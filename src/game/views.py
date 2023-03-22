from django import forms, http
from django.views import generic

from . import forms, models


class Home(generic.TemplateView):
    template_name = "home.html"


class CharacterCreation(generic.FormView):
    template_name = "character-creation.html"
    form_class = forms.CharacterCreationForm
    success_url = "/"

    def form_valid(self, form: forms.CharacterCreationForm) -> http.HttpResponse:
        if form.is_valid():
            models.Character.objects.create(
                name=form.cleaned_data["name"],
                race_name=form.cleaned_data["race_name"],
                class_name=form.cleaned_data["class_name"],
                visual_description=form.cleaned_data["visual_description"],
                personality=form.cleaned_data["personality"],
                backstory=form.cleaned_data["backstory"],
            )

        return super().form_valid(form)
