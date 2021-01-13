from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('find', views.find_recipe, name='find'),
    path('how-to-use', views.how_to_use, name='how'),
    path('about', views.about, name='about'),
    path('bad', views.bad, name='bad')
]
