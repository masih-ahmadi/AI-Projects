from django.urls import path
from .views import module_query_view

urlpatterns = [
    path('query/', module_query_view, name='module_query'),
]
