from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages as django_messages
from .models import UploadedFile, Message
from django.http import HttpResponseForbidden, JsonResponse
import os
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import json

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

def get_chat_history(user):
    # Convert database messages to format needed for Groq
    messages = []
    for msg in Message.objects.filter(user=user).order_by('timestamp'):
        if msg.is_bot:
            messages.append(AIMessage(content=msg.content))
        else:
            messages.append(HumanMessage(content=msg.content))
    return messages

@login_required
def chat_home(request):
    # Get user's chat history
    chat_messages = Message.objects.filter(user=request.user).order_by('timestamp')
    
    if not chat_messages.exists():
        # Create initial bot message for new users
        Message.objects.create(
            user=request.user,
            content="Hi, I'm your mental health counselor. How can I help you today?",
            is_bot=True
        )
        chat_messages = Message.objects.filter(user=request.user)
    
    context = {
        'chat_messages': chat_messages,
        'user': request.user,
        'hide_navbar': True
    }
    return render(request, 'chat/chat_home.html', context)

@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if user_message:
                # Save user message
                Message.objects.create(
                    user=request.user,
                    content=user_message,
                    is_bot=False
                )
                
                # Get chat history and prepare for Groq
                chat_history = get_chat_history(request.user)
                groq_messages = [
                    SystemMessage(content="You are a helpful mental health counselor chatbot."),
                    *chat_history
                ]
                
                try:
                    # Get response from Groq
                    response = llm.invoke(groq_messages)
                    bot_message = str(response.content)
                    
                    # Save bot response
                    Message.objects.create(
                        user=request.user,
                        content=bot_message,
                        is_bot=True
                    )
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': bot_message,
                        'user_message': user_message
                    })
                except Exception as e:
                    print(f"Error getting response from Groq: {e}")
                    error_message = "I apologize, but I'm having trouble processing your request right now. Please try again."
                    Message.objects.create(
                        user=request.user,
                        content=error_message,
                        is_bot=True
                    )
                    return JsonResponse({
                        'status': 'error',
                        'message': error_message,
                        'user_message': user_message
                    })
            
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
        django_messages.success(request, 'File uploaded successfully!')
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
            django_messages.success(request, 'File deleted successfully!')
        except UploadedFile.DoesNotExist:
            django_messages.error(request, 'File not found!')
    return redirect('admin_dashboard') 