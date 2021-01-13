import json

from ..parser.handler import CommandHandler


class RecipeContainer:
    def __init__(self, links):
        self.recipe_links = links
        self.recipes = []
        self.handler = CommandHandler()

    def parse_all_recipes(self):
        for link in self.recipe_links:
            self.handler.set_new_host(link)
            recipe = json.loads(self.handler.get_dto())
            self.recipes.append(recipe)
