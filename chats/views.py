from django.shortcuts import render, redirect, get_object_or_404
from chats.models import Chat
from django.http import HttpResponse
from django.urls import reverse

# imports for chatbot
from chats.Chatbot import Chatbot

import re

#for text to speech
import pyttsx3

#for text to be copied to clipboard
# import pyperclip
import os


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

    chatbot = Chatbot(api_key = '')
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


# for text to speech
def read_aloud(request, pk):
    chat = get_object_or_404(Chat, pk = pk)
    text_to_speech(chat.bot_response)
    return redirect('home')

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# for text to be copied to clipboard
def copy_to_clipboard(request, pk):
    chat = get_object_or_404(Chat, pk = pk)
    
    # two methods to copy to clipboard
    # pyperclip.copy(chat.bot_response)  # external library
    os.system("echo " + chat.bot_response.strip() + "| clip")  # using os
    return redirect('home')
