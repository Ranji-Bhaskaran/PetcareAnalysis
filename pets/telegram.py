""" Program for sending message to Telegram """
import requests

def send_adoption_message(pet_name, pet_image_url):
    """ Function for sending message to Telegram """
    telegram_bot_token = '7763482854:AAHt8ejakW8Q1ptl0QRQFKaX13smdymMBK8'
    chat_id = '1505962081'  # Your chat ID

    # Construct the message
    message = f"Congratulations! A user has adopted {pet_name}.\nImage: {pet_image_url}"

    # Send message with image to Telegram
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'caption': message,
        'photo': pet_image_url  # Imgur URL as the photo link
    }

    try:
        response = requests.post(url, data=payload, timeout=10)  # Added timeout
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        print("Message and photo sent successfully!")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
