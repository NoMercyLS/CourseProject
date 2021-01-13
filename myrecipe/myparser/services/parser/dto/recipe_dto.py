import json


class RecipeDto:
    def __init__(self, title="Unknown recipe",
                 energy_value=0,
                 serving_count=0,
                 cooking_time=0,
                 source_link="Unknown url",
                 img_url="Unknown url",
                 ingredients=None,
                 steps=None
                 ):
        if steps is None:
            steps = []
        self.title = title
        self.energy_value = energy_value
        self.serving_count = serving_count
        self.cooking_time = cooking_time
        self.source_link = source_link
        self.img_url = img_url
        self.ingredients = ingredients
        self.steps = steps

    def to_string(self):
        output = str()
        output += "Title: " + self.title + '\n'
        output += "Energy value: " + str(self.energy_value) + '\n'
        output += "Servings count: " + str(self.serving_count) + '\n'
        output += "Cooking time: " + str(self.cooking_time) + '\n'
        output += "Source link: " + self.source_link + '\n'
        output += "Image: " + self.img_url + '\n'
        output += "Steps: " + '\n'
        for step in self.steps:
            output += step["stepDescription"] + '\n'
        output += "Products: " + '\n'
        for ingredient in self.ingredients:
            output += ingredient["ingredient"]["title"] + " - " \
                      + str(ingredient["quantity"]) \
                      + ' ' + ingredient["unit"]["title"] + '\n'
        return output

    def to_json(self):
        return json.dumps({
            "title": str(self.title),
            "energyValue": int(self.energy_value),
            "servingsCount": int(self.serving_count),
            "cookingTime": int(self.cooking_time),
            "src": str(self.source_link),
            "img_url": str(self.img_url),
            "instructions": self.steps,
            "products": self.ingredients
        }, ensure_ascii=False, indent=2)
