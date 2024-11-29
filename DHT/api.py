from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from twilio.rest import Client
import requests

# Keys and configuration
TWILIO_ACCOUNT_SID = "AC931398dee75ca6dd52d7ca3687cbf3ca"
TWILIO_AUTH_TOKEN = "2f178a89ecccc08144b4523d17a4adeb"
TELEGRAM_TOKEN = "8189873848:AAHjA2lUqYE5VBJG3Zu3O1rsEsL64c-IAKQ"
TELEGRAM_CHAT_ID = "1564039415"
EMAIL_HOST_USER = "anassbenomar27@gmail.com"


# Function to send Telegram messages
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Erreur Telegram: {response.text}")
    return response


@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(f"Dernière température enregistrée : {derniere_temperature}")

            # Check if the temperature exceeds the threshold
            if derniere_temperature > 25:
                alert_message = (
                    "La température dépasse le seuil de 25°C, "
                    "veuillez intervenir immédiatement pour vérifier et corriger cette situation."
                )

                # Send alert via Email
                try:
                    send_mail(
                        subject="Alerte de Température",
                        message=alert_message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=['anassbenomar27@gmail.com'],
                    )
                except Exception as e:
                    print(f"Erreur lors de l'envoi de l'email : {e}")

                # Send alert via WhatsApp
                try:
                    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    client.messages.create(
                        from_='whatsapp:+14155238886',
                        body=alert_message,
                        to='whatsapp:+212641097356'
                    )
                except Exception as e:
                    print(f"Erreur lors de l'envoi du message WhatsApp : {e}")

                # Send alert via Telegram
                try:
                    send_telegram_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, alert_message)
                except Exception as e:
                    print(f"Erreur lors de l'envoi du message Telegram : {e}")

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
