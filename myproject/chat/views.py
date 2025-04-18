from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import UploadedFile
from django.http import HttpResponseForbidden
import os
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, filter_messages
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq API
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=32767,
    timeout=10,
    max_retries=2,
)

def get_initial_messages():
    # Define initial messages for the chat
    return [
        {
            'content': "Hi, I'm your mental health counselor. How can I help you today?",
            'name': "Counselor",
            'type': 'ai'
        }
    ]

def convert_to_langchain_message(message):
    if message['type'] == 'human':
        return HumanMessage(content=message['content'])
    else:
        return AIMessage(content=message['content'])

@login_required
def chat_home(request):
    # Get messages from session or initialize
    messages = request.session.get('chat_messages', get_initial_messages())
    
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            # Add user message
            messages.append({
                'content': user_message,
                'name': request.user.username,
                'type': 'human'
            })
            
            # Convert messages for Groq
            groq_messages = [
                SystemMessage(content="You are a helpful mental health counselor chatbot."),
                *[convert_to_langchain_message(msg) for msg in messages]
            ]
            
            try:
                # Get response from Groq
                response = llm.invoke(groq_messages)
                # Add AI response
                messages.append({
                    'content': str(response.content),
                    'name': "Counselor",
                    'type': 'ai'
                })
            except Exception as e:
                print(f"Error getting response from Groq: {e}")
                messages.append({
                    'content': "I apologize, but I'm having trouble processing your request right now. Please try again.",
                    'name': "Counselor",
                    'type': 'ai'
                })
            
            # Store messages in session
            request.session['chat_messages'] = messages
            request.session.modified = True
    
    context = {
        'messages': messages,
        'user': request.user,
        'hide_navbar': True
    }
    return render(request, 'chat/chat_home.html', context)

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        new_file = UploadedFile(
            name=uploaded_file.name,
            file=uploaded_file,
            size=uploaded_file.size
        )
        new_file.save()
        messages.success(request, 'File uploaded successfully!')
        return redirect('admin_dashboard')

    files = UploadedFile.objects.all()
    return render(request, 'admin/dashboard.html', {'files': files})

@user_passes_test(is_admin)
def delete_file(request, file_id):
    if request.method == 'POST':
        try:
            file = UploadedFile.objects.get(id=file_id)
            file.file.delete()  # Delete the actual file
            file.delete()  # Delete the database record
            messages.success(request, 'File deleted successfully!')
        except UploadedFile.DoesNotExist:
            messages.error(request, 'File not found!')
    return redirect('admin_dashboard') 