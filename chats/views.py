from django.shortcuts import render, redirect
from chats.models import Chat
from django.http import HttpResponse

# imports for chatbot
from chats.Chatbot import Chatbot

import re


# Create your views here.
def sendChat(request):
    user_input = request.POST['prompt_user']
    Chat.objects.create(
        user_prompt = user_input,
        bot_response = generate_gemini_response(user_input),
    )

    return redirect('home')


# function for response generation
def generate_gemini_response(user_input):

    chatbot = Chatbot(api_key = 'AIzaSyBS4fBmpCv7UYTD9bksmTPpmlxoN8y7xkQ')
    chatbot.start_conversation()

    state = True
    while state:
        if user_input.lower() == 'quit':
            state = False
            return 'Bye'

        try:
            response = chatbot.send_prompt(user_input)[10:-2]
            # response = identify_formatting(response)
            return (f"{response}") # because is a response string, not dictionary
        except Exception as e:
            return (f"Error: {e}")
        

def identify_formatting(response):
    # Identify bold strings enclosed in ** **
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    # Identify line breaks and replace with <br> tags
    response = response.replace('\n', '<br>')
    return response