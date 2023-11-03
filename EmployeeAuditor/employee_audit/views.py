from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from .models import EmployeeAudit
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse_lazy
import psutil
import json
import logging

# Importaciones de Modelos

from .models import Empleado, EmployeeAudit, Proyecto, Notificacion, Mensaje, Tarea, TareaXEmpleado
from .forms import EmpleadoForm, NotificacionForm, ProyectForm,TaskXEmployeeForm

# Importaciones de CBV
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.views import LoginView

class HomeView(TemplateView):
    template_name = 'employee_audit/home.html'
    
def acerca_view(request):
    return render(request, 'employee_audit/acerca.html')


#Tareas------------------------------
class TaskList(ListView):
    model = TareaXEmpleado

class TaskCreate(CreateView):
    model = Tarea
    form_class = TaskXEmployeeForm
    template_name = 'employee_audit/tarea_x_empleado_form.html'
    success_url = '/tareas/'

class TaskSearch(ListView):
    model = TareaXEmpleado
    template_name = 'employee_audit/task_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return TareaXEmpleado.objects.filter(
                Q(empleado__nombre__icontains=query) | Q(tarea__descripcion__icontains=query)
            )
        else:
            return TareaXEmpleado.objects.all()
#------------------------------------
#Proyect-----------------------------
class ProyectList(ListView):
    model = Proyecto

class ProyectCreate(CreateView):
    model = Proyecto
    form_class = ProyectForm
    success_url = reverse_lazy("proyectos")
#------------------------------------
#Notification------------------------
class NotificationList(ListView):
    model = Notificacion

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["titulo"] = "Lista de notificaciones enviadas"
        return contexto
    
class NotificationCreate(CreateView):
    model = Notificacion
    form_class = NotificacionForm
    success_url = reverse_lazy("notificaciones")

    def form_valid(self, form):
        # Obtener el mensaje seleccionado o crear uno nuevo
        nuevo_mensaje = form.cleaned_data.get('nuevo_mensaje')
        if nuevo_mensaje:
            mensaje = Mensaje.objects.create(contenido=nuevo_mensaje)
            form.instance.mensaje = mensaje
        return super().form_valid(form)
#-----------------------------------
#Employee---------------------------
class EmployeeList(ListView):
    model = Empleado

class EmployeeCreate(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy("empleados")

class EmployeeUpdate(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('empleados-actualizar', args = [self.object.id])+"?ok"
#-----------------------------------

logger = logging.getLogger('csf_token_logger')

#Activity Tracker-------------------
#Define un default para el activity tracker
current_data = {
    'active_app': "Desconectado",
    'activity_description': "Descripción de la actividad",
}

#Captura la aplicación actual y recibe los datos del seeker en C#
@csrf_exempt
def capture_active_app(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            #Actualiza los datos actuales con los nuevos datos
            current_data['active_app'] = data.get('active_app', "Desconectado")
            current_data['activity_description'] = data.get('activity_description', "Descripción de la actividad")
            #Registra los datos recibidos
            logger.info(f"Datos recibidos: {data}")
        except json.JSONDecodeError:
            #Manejar un error si los datos JSON no son válidos
            return JsonResponse({'error': 'Datos JSON no válidos'}, status=400)

    #Crea un diccionario con los datos actuales para enviar como respuesta JSON a your_js_file.js
    response_data = {
        'active_app': current_data['active_app'],
        'activity_description': current_data['activity_description'],
    }

    return JsonResponse(response_data)




def get_csrf_token(request):
    return JsonResponse({'csrf_token': request.COOKIES.get('csrftoken')})


def activity_page(request):
    return render(request, 'employee_audit/activity_template.html')