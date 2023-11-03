from django.db import models

#Modelo de Activity Tracker, es necesario agregar un empleado Foraneo y normalizar la descripción de las aplicaciones
class EmployeeAudit(models.Model):
    employee_name = models.CharField(max_length=100)
    application_name = models.CharField(max_length=100)
    activity_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

#Modelo del mensaje, usado para la notificación.
class Mensaje(models.Model):
    contenido = models.CharField(verbose_name="Mensajes", max_length=500)

    def __str__(self):
        return self.contenido

#Modelo del Proyecto, expande la utilidad de las tareas
class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Proyectos", max_length=100)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self) -> str:
        return self.nombre

#Modelo del Empleado, define empleados activos e inactivos
class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(verbose_name="Empleados", max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    edad = models.PositiveIntegerField(verbose_name="Edad", blank=True, null= True)
    direccion = models.CharField(max_length=255, blank=True, null= True)
    telefono = models.CharField(max_length=15, blank=True, null= True)
    email = models.EmailField(max_length=100, blank=True, null= True)
    fecha_de_ingreso = models.DateField(verbose_name="Fecha de Ingreso", blank=True, null= True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
            return self.nombre

#Modelo de Tarea, una tarea puede o no tener un Proyecto asignado, pero siempre tendrá un empleado Foraneo
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(verbose_name="Descripción de la tarea", default="Tarea sin descripción")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return self.descripcion

class TareaXEmpleado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tarea por Empleado"
        verbose_name_plural = "Tareas por Empleados"

    def __str__(self):
        return f"{self.empleado.nombre} - {self.tarea.descripcion}"
#Modelo de Notificación, muestra el contenido de un mensaje, por normalización, a solo un empleado
class Notificacion(models.Model):
    id = models.AutoField(primary_key=True)
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name='notificaciones', default=1)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='notificaciones')
    fecha_envio = models.DateTimeField(auto_now_add=True, null= True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"Notificación {self.id}"