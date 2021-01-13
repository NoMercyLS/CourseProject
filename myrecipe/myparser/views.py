from django.shortcuts import redirect, render

# Create your views here.
from .forms import RecipeFinder
from .services.parser.handler import CommandHandler
from .services.recipe_container.container import RecipeContainer

import json


def index(request):
    return render(request, 'myparser/index.html')


def find_recipe(request):
    if request.method == 'POST':
        form = RecipeFinder(request.POST)
        if form.is_valid():
            line = request.POST['search']
            handler = CommandHandler()
            if "https" in line:
                try:
                    handler.set_new_host(line)
                    context = json.loads(handler.get_dto())
                    return render(request, 'myparser/recipe.html', context)
                except Exception as e:
                    print(e)
            else:
                try:
                    container = RecipeContainer(handler.find_recipes(line))
                    container.parse_all_recipes()
                    context = {
                        'recipes': container.recipes
                    }
                    return render(request, 'myparser/recipes.html', context)
                except Exception as e:
                    print(e)
    else:
        form = RecipeFinder()
        context = {
            'form': form
        }
        return render(request, 'myparser/find.html', context)


def how_to_use(request):
    return render(request, 'myparser/how.html')


def about(request):
    return render(request, 'myparser/about.html')


def bad(request):
    return render(request, 'myparser/bad.html')
