from django.views import generic

from . import domain


class CharacterCreation(generic.TemplateView):
    template_name = "character-creation.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        ctx = super().get_context_data(**kwargs)

        # Get character description
        character_description = domain.get_openai_character_description()
        ctx["name"] = character_description.name
        ctx["race"] = character_description.race
        ctx["class"] = character_description.class_
        ctx["visual_description"] = character_description.visual_description
        ctx["personality"] = character_description.personality
        ctx["backstory"] = character_description.backstory
        ctx["full_description"] = character_description.full_description

        return ctx
