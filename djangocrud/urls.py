"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='Home'),
    path('signup/',views.signup,name='signup'),
    path('task/',views.task,name='task'),
    path('loguin/',views.loguin,name='loguin'),
    path('logout/',views.signout,name='logout'),
    path("change_password/", views.change_password, name="cambiar_password"),
    path('suma/', views.suma,name='suma'),
    path('resta/', views.resta,name='resta'),
    path('multiplicacion/', views.multiplicacion,name='multiplicacion'),
    path('escalar/', views.escalar,name='escalar'),
    path('gauss/',  views.gauss,name='gauss'),
    path('gauss_jordan/', views.gauss_jordan,name='gauss_jordan'),
    path('transpuesta/', views.transpuesta,name='transpuesta'),
    path('determinante/', views.determinante,name='determinante'),
    path('inversa/', views.inversa,name='inversa'),
    path('elevar/', views.elevar,name='elevar'),
    path('operaciones/', views.operaciones,name='operaciones'),
    path('SEL/',views.SEL,name='SEL'),
    path('accounts/', include('allauth.urls')),
    path('confirm_email/',views.confirm_email,name='confirm_email'),
    path('confirm_code/',views.confirm_code,name='confirm_code'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_conversation'),
    path('chat/new/', views.new_conversation, name='new_conversation'),
    path('chat/delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('cramer/',views.cramer,name='cramer'),
    path('elim_gauss/',views.elim_gauss,name='elim_gauss'),
    path('elim_gauss_jordan/',views.elim_gauss_jordan,name='elim_gauss_jordan'),
    path('jacobi/',views.jacobi,name='jacobi'),
]
