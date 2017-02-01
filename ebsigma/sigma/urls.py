from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^results/(?P<uid>[^/]+)/', views.results, name='results'),
  url(r'^$', views.index, name='index'),
]
