import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User

print("Iniciando creación de superusuario...")

# Datos del superusuario
username = 'ryuya'
email = 'armasyaniel@gmail.com'
password = 'admin123'

try:
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f"El usuario '{username}' ya existe. Eliminando...")
        User.objects.filter(username=username).delete()
        print("Usuario anterior eliminado.")
    
    # Crear superusuario
    print("Creando nuevo superusuario...")
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print("\n" + "="*60)
    print("✅ SUPERUSUARIO CREADO EXITOSAMENTE")
    print("="*60)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("="*60)
    print("\n🌐 Inicia el servidor con: python manage.py runserver")
    print("🔗 Luego ve a: http://127.0.0.1:8000/admin")
    print("\n")
    
except Exception as e:
    print("\n❌ ERROR al crear superusuario:")
    print(str(e))
    import traceback
    traceback.print_exc()