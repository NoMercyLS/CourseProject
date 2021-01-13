import random

import requests
import validators
from bs4 import BeautifulSoup

from .hosts import artlunchru, edaru


class CommandHandler:
    def __init__(self):
        self.host = "vk.com"
        self.allowed_resources = [
            "https://eda.ru/recepty/",
            "https://www.gastronom.ru/recipe/",
            "https://art-lunch.ru/recipe/"
        ]
        self.is_default = True
        self.is_error_encountered = False

    def set_new_host(self, new_host_url):
        if self.is_default:
            self.is_default = False
        self.host = new_host_url

    def is_allowed(self):
        if validators.url(self.host):
            for resource in self.allowed_resources:
                if resource in self.host:
                    if len(resource) < len(self.host):
                        try:
                            req = requests.get(self.host).status_code
                            if req == 200:
                                return True
                            else:
                                return False
                        except Exception as e:
                            print(self.host)
                            print("Failed to reach the host. Error info: ", e)
                            return False
                    else:
                        return False
        return False

    def get_resource(self):
        for resource in self.allowed_resources:
            if resource in self.host:
                return resource
        return None

    @staticmethod
    def find_recipes(search_string):
        try:
            edaru_link = "https://eda.ru/recipesearch?q=" + search_string.replace(' ', '+') + "=&onlyEdaChecked=false"
            edaru_html = requests.get(edaru_link, allow_redirects=False)
            edaru_html.encoding = 'utf-8'
            edaru_formatted = BeautifulSoup(edaru_html.text, features="html.parser")
            edaru_recipes = edaru_formatted.find_all("div", {"class": "js-bookmark__obj"})

            artlunch_link = "https://art-lunch.ru/?s=" + search_string.replace(' ', '+')
            artlunch_html = requests.get(artlunch_link, allow_redirects=False)
            artlunch_html.encoding = 'utf-8'
            artlunch_formatted = BeautifulSoup(artlunch_html.text, features="html.parser")
            artlunch_recipes = artlunch_formatted.find_all("div", {"class": "col-sm-6"})

            recipe_urls = []

            if edaru_recipes:
                index = 0
                for recipe in edaru_recipes:
                    if index < 10:
                        index += 1
                    else:
                        break
                    recipe_urls.append("https://eda.ru" + recipe.find("h3").find("a").get("href"))
            if artlunch_recipes:
                index = 0
                for recipe in artlunch_recipes:
                    if index < 10:
                        index += 1
                    else:
                        break
                    recipe_urls.append(recipe.find("a").get("href"))

            random.shuffle(recipe_urls)

            return recipe_urls

        except Exception as e:
            print(e)
            return None

    def get_dto(self):
        if self.is_allowed():
            if self.get_resource() == self.allowed_resources[0]:
                eda = edaru.EdaRu(self.host)
                try:
                    return eda.get_recipe_json()
                except Exception as e:
                    print(e)
                    pass
            # if self.get_resource() == self.allowed_resources[1]:
            #     gastronom = gastronomru.GastronomRu(self.host)
            #     try:
            #       return gastronom.get_recipe_dto()
            #     except:
            #         pass
            if self.get_resource() == self.allowed_resources[2]:
                artlunch = artlunchru.ArtLunchRu(self.host)
                try:
                    return artlunch.get_recipe_json()
                except Exception as e:
                    print(e)
                    pass
            raise Exception('Recipe not found! Link is incorrect.\nPlease, enter new link')
        else:
            if self.host == "!exit":
                exit(0)
            else:
                raise Exception('Incorrect source link, try again\nTo finish, write !exit')
