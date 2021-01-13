import re

import requests
from bs4 import BeautifulSoup

from ..converter import *
from ..dto import recipe_dto


class ArtLunchRu:
    def __init__(self, src):
        self.main_url = "https://art-lunch.ru/"
        self.src = src
        self.html_document = self.get_html_file()

    def get_html_file(self):
        html = requests.get(self.src, allow_redirects=False)
        html.encoding = 'utf-8'
        return BeautifulSoup(html.text, features="html.parser")

    def get_recipe_json(self):
        # Build recipe object
        recipe_obj = recipe_dto.RecipeDto(self.get_title(),
                                          self.get_calories_amount(),
                                          self.get_serving_count(),
                                          convert_time(
                                              self.get_cooking_time()
                                          ),
                                          self.src,
                                          self.get_image_src(),
                                          self.get_ingredients(),
                                          self.get_steps())
        return recipe_obj.to_json()

    def get_steps(self):
        steps = self.html_document.find("div", {"id": "recipeInstructions"}).find_all("p")
        instruction = []
        for step in steps:
            instruction.append({
                "stepDescription": step.text.replace('\n', '')
            })
        return instruction

    def get_title(self):
        title = self.html_document.find("h1").contents[0]
        title = ' '.join(title.split())
        return title

    def get_image_src(self):
        img_src = self.html_document.find("img", {"itemprop": "resultPhoto"}).get("src")
        return img_src

    def get_calories_amount(self):
        return self.html_document.find("span", {"itemprop": "calories"}).contents[0].split()[0]

    def get_serving_count(self):
        return self.html_document.find("span", {"itemprop": "recipeYield"}).contents[0].split()[0][0]

    def get_ingredients(self):
        ingredients = []
        ing = self.html_document.find_all("span", {"itemprop": "recipeIngredient"})
        for ingredient in ing:
            ingredient_name = re.sub('[^А-я^0-9 -ё]', '', ingredient.contents[0].strip())
            ingredient_quantity_unit = re.sub('[^А-я^0-9 .ё/-]', '', ingredient.contents[1].text.strip())
            ingredient_quantity = None
            ingredient_unit = None
            try:
                if ingredient_quantity_unit in quantity_library:
                    ingredient_quantity = None
                    ingredient_unit = ingredient_quantity_unit
                else:
                    ingredient_quantity = get_calculated_quantity(ingredient_quantity_unit.split()[0])
                    ingredient_unit = get_replaced_unit(ingredient_quantity_unit.split()[1])
            except:
                ingredient_quantity = None
                ingredient_unit = "по вкусу"
            finally:
                ingredients.append({
                    "ingredient":
                        {
                            "title": str(ingredient_name)
                        },
                    "quantity": ingredient_quantity,
                    "unit":
                        {
                            "title": str(ingredient_unit)
                        }
                })

        return ingredients

    def get_cooking_time(self):
        cooking_time = self.html_document.find("div", {"class": "small"}).find("span")
        if cooking_time is None:
            return None
        return cooking_time.contents[0].split()
