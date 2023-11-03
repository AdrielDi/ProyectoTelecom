from django import forms
from .models import Empleado, Notificacion, Mensaje, Proyecto, TareaXEmpleado, Tarea
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'estado', 'edad', 'direccion', 'telefono', 'email', 'fecha_de_ingreso']
        
        ESTADO_CHOICES = [
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
        ]
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Empleado'}),
            'estado': forms.Select(choices=ESTADO_CHOICES, attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'fecha_de_ingreso': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de Ingreso'}),
        }
        
        labels = {
            'nombre': "",
            'estado': "Estado",
        }

        help_texts = {
            'estado': "Selecciona el estado del empleado",
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Empleado'}),
            'estado': forms.Select(choices=ESTADO_CHOICES, attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'fecha_de_ingreso': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de Ingreso'}),
        }

class NotificacionForm(forms.ModelForm):
    nuevo_mensaje = forms.CharField(
        max_length=500,
        required=False,
        label="Nuevo Mensaje",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Notificacion
        fields = ['empleado', 'nuevo_mensaje']

    def __init__(self, *args, **kwargs):
        super(NotificacionForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].widget.attrs['class'] = 'form-control'
        self.fields['nuevo_mensaje'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(NotificacionForm, self).clean()
        nuevo_mensaje = cleaned_data.get('nuevo_mensaje')

        # Verificar si se proporcionó un nuevo mensaje o si se seleccionó uno existente.
        if not nuevo_mensaje:
            mensaje = cleaned_data.get('empleado')
        else:
            # Crear un nuevo mensaje si se proporciona uno nuevo.
            mensaje = Mensaje.objects.create(contenido=nuevo_mensaje)

        return cleaned_data
    
class ProyectForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre']

    widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Proyecto'}),
    }

    labels = {
        'nombre': 'Nombre del Proyecto',
    }

    help_texts = {
        'nombre': 'Ingresa el nombre del proyecto',
    }

class TaskXEmployeeForm(forms.ModelForm):
    empleados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.filter(estado='Activo'),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Tarea
        fields = ['descripcion', 'proyecto']

    def save(self, commit=True):
        tarea = super(TaskXEmployeeForm, self).save(commit=False)
        if commit:
            tarea.save()
        for empleado in self.cleaned_data['empleados']:
            tarea_x_empleado = TareaXEmpleado(empleado=empleado, tarea=tarea)
            tarea_x_empleado.save()
        return tarea