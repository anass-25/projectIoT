from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
# Définir la fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response
@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            if serial.is_valid():
                serial.save()
                derniere_temperature = Dht11.objects.last().temp
                print(derniere_temperature)

                if derniere_temperature > 15:
                    # Alert Email
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['anassbenomar27@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)


                    # Alert WhatsApp
                    account_sid = 'AC931398dee75ca6dd52d7ca3687cbf3ca'
                    auth_token = '2f178a89ecccc08144b4523d17a4adeb'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                        to='whatsapp:+212641097356'
                    )

                    # Alert Telegram
                    telegram_token = '8189873848:AAHjA2lUqYE5VBJG3Zu3O1rsEsL64c-IAKQ'
                    chat_id = '1564039415'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)

                return Response(serial.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

account_sid = 'AC931398dee75ca6dd52d7ca3687cbf3ca'
auth_token = '2f178a89ecccc08144b4523d17a4adeb'
client = Client(account_sid, auth_token)
message = client.messages.create(
from_='whatsapp:+14155238886',
body='La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
to='whatsapp:+212641097356'
)



