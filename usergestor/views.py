from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Usuario, CustomUser
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomUserChangeForm , UserCreationForm, AdminUserCreationForm
from django.contrib.auth.models import User,Group
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Manejar el caso de error
            return render(request, 'registration/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'registration/login.html')

@login_required
def personasIndex(request):

    if request.user.is_superuser:
        return render(request, 'dashboard/dashboardadmin.html')
    if request.user.is_staff:
        return render(request, 'dashboard/dashboardstaff.html')
    else:
        return render(request, 'dashboard/dashboarduser.html')
    

def signUp(request):
    usuario = Usuario
    form = SignUpForm
    if request.method == 'POST':
        print("POST")
        form = SignUpForm(request.POST)
        """ Mostrar data del form """
        if form.is_valid():
            print("VALIDO")	
            form.save()
            return redirect('/')
        else:
            print("NO VALIDO")
            print(form.errors)	

    return render(request, 'registration/signUp.html', {'form': form})

def is_super_user(user):
    return user.is_superuser

@login_required
@user_passes_test(is_super_user)
def manage_users(request, pk=None):
    if request.method == 'POST':
        if 'edit' in request.POST:
            user = User.objects.get(pk=pk)
            form = CustomUserChangeForm(request.POST, instance=user)
            action = 'edit'
        elif 'delete' in request.POST:
            User.objects.get(pk=pk).delete()
            return redirect('manage_users')

        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = CustomUserCreationForm() if pk is None else CustomUserChangeForm(instance=User.objects.get(pk=pk))
        action = 'edit' if pk else 'create'

    users = User.objects.all()
    return render(request, 'admin/usergestor.html', {'users': users, 'form': form, 'action': action})


def is_admin(user):
    return user.is_superuser
@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Asignar el usuario a un grupo basado en la selección del formulario
            role = form.cleaned_data.get('role')
            if role == 'admin':
                group = Group.objects.get(name='Administrador') # Asegúrate de que este grupo exista
                user.groups.add(group)
            elif role == 'staff':
                group = Group.objects.get(name='Supervisor') # Asegúrate de que este grupo exista
                user.groups.add(group)
            # No es necesario agregar al grupo para usuarios normales, a menos que tengas un grupo específico para ellos

            return redirect("{% url 'dashboard' %}")
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin/usercreator.html', {'form': form})