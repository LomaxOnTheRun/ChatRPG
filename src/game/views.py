from django.views import generic


class CharacterCreation(generic.TemplateView):
    template_name = "character-creation.html"
