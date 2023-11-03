from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path("proyectos/", ProyectList.as_view(), name="proyectos"),
    path("proyectos_crear/", ProyectCreate.as_view(), name="proyectos-crear"),

    path("tareas/", TaskList.as_view(), name="tareas"),
    path('tarea_x_empleado_crear/', TaskCreate.as_view(), name='tarea_x_empleado-crear'),
    path('tasks/search/', TaskSearch.as_view(), name='task_search'),

    path("notificaciones/", NotificationList.as_view(), name="notificaciones"),
    path("notificaciones_crear/", NotificationCreate.as_view(), name="notificaciones-crear"),

    path("empleados/", EmployeeList.as_view(), name="empleados"),
    path("empleados_crear/", EmployeeCreate.as_view(), name="empleados-crear"),
    path("empleados_actualizar/<int:pk>/", EmployeeCreate.as_view(), name="empleados-actualizar"),

    path('capture_active_app/', views.capture_active_app, name='capture_active_app'),
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('activity/', views.activity_page, name='activity_page'),

    path('acerca/', views.acerca_view, name='acerca'),
]
