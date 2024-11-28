from django.shortcuts import render
from .models import Dht11 # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm


def test(request) :
 return HttpResponse('hello')


def table(request):
 derniere_ligne = Dht11.objects.last()
 derniere_date = derniere_ligne.dt  # Utilisation directe de derniere_ligne pour éviter des requêtes répétées
 delta_temps = timezone.now() - derniere_date
 difference_minutes = delta_temps.seconds // 60
 temps_ecoule = 'il y a ' + str(difference_minutes) + ' min'

 if difference_minutes > 60:
  temps_ecoule = 'il y a ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + ' min'

 valeurs = {
  'date': temps_ecoule,
  'id': derniere_ligne.id,
  'temp': derniere_ligne.temp,
  'hum': derniere_ligne.hum
 }

 return render(request, 'value.html', {'valeurs': valeurs})


def download_csv(request):
 model_values = Dht11.objects.all()
 response = HttpResponse(content_type='text/csv')
 response['Content-Disposition'] = 'attachment; filename="dht.csv"'
 writer = csv.writer(response)

 # Écrire les en-têtes des colonnes
 writer.writerow(['id', 'temp', 'hum', 'dt'])

 # Récupérer les valeurs de chaque instance de Dht11
 liste = model_values.values_list('id', 'temp', 'hum', 'dt')
 for row in liste:
  writer.writerow(row)

 return response

def graphiqueTemp(request):
  return render(request, 'ChartTemp.html')


# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def graphiqueHum(request):
 return render(request, 'ChartHum.html')


def chart_data(request):
 dht = Dht11.objects.all()

 data = {
  'temps': [Dt.dt for Dt in dht],
  'temperature': [Temp.temp for Temp in dht],
  'humidity': [Hum.hum for Hum in dht]
 }
 return JsonResponse(data)

def chart_data_jour(request):
  dht = Dht11.objects.all()
  now = timezone.now()

  # Récupérer l'heure il y a 24 heures
  last_24_hours = now - timezone.timedelta(hours=24)

  # Récupérer tous les objets de Module créés au cours des 24 dernières heures
  dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
  data = {
   'temps': [Dt.dt for Dt in dht],
   'temperature': [Temp.temp for Temp in dht],
   'humidity': [Hum.hum for Hum in dht]
  }
  return JsonResponse(data)


# pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
 dht = Dht11.objects.all()
 # calcul de la date de début de la semaine dernière
 date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
 print(datetime.timedelta(days=7))
 print(date_debut_semaine)

 # filtrer les enregistrements créés depuis le début de la semaine dernière
 dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

 data = {
  'temps': [Dt.dt for Dt in dht],
  'temperature': [Temp.temp for Temp in dht],
  'humidity': [Hum.hum for Hum in dht]
 }

 return JsonResponse(data)


# pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
 dht = Dht11.objects.all()

 date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
 print(datetime.timedelta(days=30))
 print(date_debut_semaine)

 # filtrer les enregistrements créés depuis le début de la semaine dernière
 dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

 data = {
  'temps': [Dt.dt for Dt in dht],
  'temperature': [Temp.temp for Temp in dht],
  'humidity': [Hum.hum for Hum in dht]
 }
 return JsonResponse(data)


def home(request):
 return render(request, 'home.html')


def register(request):
 if request.method == 'POST':
  form = UserCreationForm(request.POST)
  if form.is_valid():
   form.save()
   return redirect('login')
 else:
  form = UserCreationForm()
 return render(request, 'register.html', {'form': form})
