from django import forms
from django.views import generic

from . import domain


class CharacterCreationForm(forms.Form):
    name = forms.CharField(label="Character name", max_length=200)
    race_name = forms.CharField(label="Race", max_length=100)
    class_name = forms.CharField(label="Class", max_length=100)
    visual_description = forms.CharField(
        label="Visual description", max_length=1000, widget=forms.Textarea
    )
    personality = forms.CharField(
        label="Personality", max_length=1000, widget=forms.Textarea
    )
    backstory = forms.CharField(
        label="Backstory", max_length=2000, widget=forms.Textarea
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

        # Get character description
        character_description = domain.get_openai_character_description()
        self.fields["name"].initial = character_description.name
        self.fields["race_name"].initial = character_description.race_name
        self.fields["class_name"].initial = character_description.class_name
        self.fields[
            "visual_description"
        ].initial = character_description.visual_description
        self.fields["personality"].initial = character_description.personality
        self.fields["backstory"].initial = character_description.backstory


class CharacterCreation(generic.FormView):
    template_name = "character-creation.html"
    form_class = CharacterCreationForm
