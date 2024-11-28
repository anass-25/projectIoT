from django.urls import path
from . import views, api

urlpatterns= [
    path("api", api.Dlist, name='json'),
    path("api/post", api.Dlist, name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/', views.table, name='table'),
    path('ChartTemp/', views.graphiqueTemp, name='myChartTemp'),
    path('ChartHum/', views.graphiqueHum, name='myChartHum'),
    path('chart-data/', views.chart_data, name='chart-data'),

    path('chart-data-jour/', views.chart_data_jour, name='chart-data-jour'),
    path('chart-data-semaine/', views.chart_data_semaine, name='chart-data-semaine'),
    path('chart-data-mois/', views.chart_data_mois, name='chart-data-mois'),
    path('', views.home, name='home'),
    ]