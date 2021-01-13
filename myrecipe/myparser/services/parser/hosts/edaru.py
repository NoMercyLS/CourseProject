import requests
from bs4 import BeautifulSoup

from ..converter import *
from ..dto import recipe_dto


class EdaRu:
    def __init__(self, src):
        self.main_url = "https://eda.ru"
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
        steps = self.html_document.find_all("span", {"itemprop": "text"})
        instruction = []
        if steps:
            for step in steps:
                instruction.append({
                    "stepDescription": ' '.join(step.contents[0].replace('\r', '').replace('\n', '').split())
                })
        else:
            steps = self.html_document.find_all("span", {"class", "instruction__description"})
            for step in steps:
                instruction.append({
                    "stepDescription": ' '.join(step.contents[3].replace('\r', '').replace('\n', '').split())
                })
        return instruction

    def get_title(self):
        title = self.html_document.find_all("h1", {"class": "recipe__name g-h1"})[0].contents[0]
        title = ' '.join(title.split())
        return title

    def get_image_src(self):
        try:
            img_src = self.html_document.find_all("div", {"class": "js-recipe-cover-img"})[0].find("img").get("src")
        except:
            img_src = self.html_document.find("div", {"class": "photo-list-preview"}).find("img").get("src")
        return img_src

    def get_calories_amount(self):
        try:
            calories_amount = self.html_document.find_all("span", {"itemprop": "calories"})[0].contents[0]
        except:
            calories_amount = self.html_document.find_all("p", {"class": "nutrition__weight"})[0].contents[0]
        return calories_amount

    def get_serving_count(self):
        default_serving_count = self.html_document.find_all("input", {"type": "number"})[0].get("value")
        return default_serving_count

    def get_ingredients(self):
        ingredients = []
        for ingredient in self.html_document.find("div", {"class": "ingredients-list layout__content-col"}).find_all(
                "p", {"class": "ingredients-list__content-item content-item "
                               "js-cart-ingredients"}):
            items = ingredient.get("data-ingredient-object").replace('"', '').replace('}', '').split(', ')
            ingredient_name = items[1].split(': ')[1]
            ingredient_quantity = None
            ingredient_unit = None
            try:
                ingredient_quantity_unit = items[2].split(': ')[1]
                if ingredient_quantity_unit in quantity_library:
                    ingredient_quantity = None
                    ingredient_unit = get_replaced_unit(ingredient_quantity_unit)
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
        cooking_time = self.html_document.find("div", {"class": "recipe__info-pad info-pad print-invisible"}) \
            .find_all("span", {"class": "info-pad__item"})[1] \
            .find_all("span")[1].contents[0].split(' ')
        return cooking_time
