from django.urls import path
from .views_compare import compare_records
from .view_summary import health_summary
from .views import search_records


urlpatterns = [
    path("compare/", compare_records),
    path("summary/", health_summary),
    path("search/", search_records),
]
