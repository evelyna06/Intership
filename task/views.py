from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from matrix_operations import MatrixOperations
from django.shortcuts import render
import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from groq import Groq
from django.conf import settings
from .models import Conversation, Message
import json

# Create your views here.

def Home(request):
 return render(request,'Home.html')

def loguin(request):
    if request.method =='GET':
       return render (request,'loguin.html',{
          'form':AuthenticationForm()
       })
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            messages.error(request, "User or password incorrect")
            return render(request,'loguin.html')
        else:
            login(request,user)
            return redirect('task')


def signup(request):
    if request.method =='GET':
       return render (request,'signup.html',{
          'form':UserCreationForm
       })
    else:
        if request.POST['password1']== request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('task')
            except IntegrityError:
                return render (request,'signup.html',{
                    'form':UserCreationForm,
                    "error":'username already exist'
                })
        return render(request,'signup.html',{
            'form':UserCreationForm,
            "error" : 'password dont not match'
        })


from django.shortcuts import render

def signout(request):
    logout(request)
    return redirect('Home')


def change_password(request):
    if request.method == "POST":
        print("Post recibido",request.POST)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Esto asi mantengo la sesion abierta despues del cambio 
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully ✅")
            return redirect("task")  # O a donde quieras redirigirlo
        else:
            messages.error(request, "Correct the errors in the form ❌")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})

def task(request):
    if request.user.is_authenticated:
        # Código para manejar la vista cuando el usuario está autenticado
        return render(request, 'task.html')
    else:
        # Si no está autenticado, redirigir o mostrar mensaje
        return redirect('login')  # O podrías devolver una respuesta personalizada

def suma(request):
 return render(request,'suma.html')
def resta(request):
 return render(request,'resta.html')
def multiplicacion(request):
 return render(request,'multiplicacion.html')
def gauss(request):
 return render(request,'gauss.html')
def gauss_jordan(request):
 return render(request,'gauss_jordan.html')
def transpuesta(request):
 return render(request,'transpuesta.html')
def determinante(request):
 return render(request,'determinante.html')
def inversa(request):
 return render(request,'inversa.html')
def elevar(request):
    return render(request,'elevar.html')
def escalar(request):
    return render(request,'escalar.html')
def operaciones(request):
    return render(request,'Operaciones_Con_Matrizes.html')
def SEL(request):
    return render(request,'SEL.html')
def confirm_email(request):
    return render(request,'confirm_email.html')
def confirm_code(request):
    return render(request,'confirm_code.html')
def cramer(request):
    return render(request,'cramer.html')
def elim_gauss(request):
    return render(request,'elim_gauss.html')
def elim_gauss_jordan(request):
    return render(request,'elim_gauss_jordan.html')
def jacobi(request):
    return render(request,'jacobi.html')





@login_required
def chat_view(request, conversation_id=None):
    # Cargar conversación si existe
    conversation = None
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            conv_id = data.get('conversation_id')
            
            # Crear o recuperar conversación
            if conv_id:
                conversation = get_object_or_404(Conversation, id=conv_id, user=request.user)
            else:
                # Nueva conversación
                title = user_message[:50] + "..." if len(user_message) > 50 else user_message
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=title
                )
            
            # Guardar mensaje del usuario
            Message.objects.create(
                conversation=conversation,
                content=user_message,
                is_user=True
            )
            
            # Obtener historial
            messages_history = list(conversation.messages.all())
            groq_messages = [
                {"role": "system", "content": "Eres un asistente útil y amigable. Responde en español."}
            ]
            
            # Agregar últimos 10 mensajes
            for msg in messages_history[-10:]:
                role = "user" if msg.is_user else "assistant"
                groq_messages.append({
                    "role": role,
                    "content": msg.content
                })
            
            # Llamar a Groq
            client = Groq(api_key=settings.GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_messages,
                temperature=0.7,
                max_tokens=1024
            )
            
            ai_response = response.choices[0].message.content
            
            # Guardar respuesta AI
            Message.objects.create(
                conversation=conversation,
                content=ai_response,
                is_user=False
            )
            
            return JsonResponse({
                'response': ai_response,
                'conversation_id': conversation.id,
                'success': True
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'success': False
            }, status=400)
    
    # GET request
    messages = []
    if conversation:
        messages = list(conversation.messages.values('content', 'is_user', 'timestamp'))
    
    user_conversations = Conversation.objects.filter(user=request.user)
    
    return render(request, 'chat.html', {
        'conversation': conversation,
        'messages': messages,
        'user_conversations': user_conversations
    })

@login_required
def new_conversation(request):
    return render(request, 'chat.html', {
        'conversation': None,
        'messages': [],
        'user_conversations': Conversation.objects.filter(user=request.user)
    })

@login_required
def delete_conversation(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        conversation.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
