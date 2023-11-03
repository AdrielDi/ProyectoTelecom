// JAVASCRIPT
$(document).ready(function () {
    // Función para obtener el token CSRF
    function getCSRFToken() {
        return $.ajax({
            url: '/get_csrf_token/',
            method: 'GET',
        });
    }

    // Función para actualizar los datos de la aplicación activa
    function updateActiveAppData() {
        // Agrega un timestamp para evitar el almacenamiento en caché del navegador
        var timestamp = new Date().getTime();
        $.ajax({
            url: '/capture_active_app/?timestamp=' + timestamp, // Agrega el timestamp a la URL
            method: 'GET',
            success: function (data) {
                // Actualiza el contenido de la etiqueta HTML con los datos recibidos
                $('#active-app-data').text(data.active_app);

                // Imprime el mensaje en la consola del navegador
                console.log('Datos recibidos:', data.active_app);
            },
            error: function () {
                // Maneja errores si es necesario
            },
        });
    }

    // Realiza la actualización de datos al cargar la página
    updateActiveAppData();

    // Realiza la actualización de datos cada cierto intervalo de tiempo (por ejemplo, cada 5 segundos)
    setInterval(updateActiveAppData, 5000); // Tiempo en milisegundos
});

$(document).ready(function () {
    // Función para enviar datos de formulario al servidor
    function createEmpleado() {
        // Obtén los datos del formulario
        var formData = $('form').serialize();

        $.ajax({
            type: 'POST',
            url: '/crear_empleado/',  // Cambia la URL de acuerdo a tu configuración
            data: formData,
            success: function (data) {
                // Maneja la respuesta del servidor, por ejemplo, muestra un mensaje de éxito
                console.log('Empleado creado con éxito:', data);
            },
            error: function (error) {
                // Maneja errores si es necesario
                console.error('Error al crear el empleado:', error);
            },
        });
    }

    // Escucha el evento clic en el botón "Crear Empleado" y llama a la función createEmpleado
    $('button[type="submit"]').on('click', function (event) {
        event.preventDefault();  // Evita que el formulario se envíe automáticamente
        createEmpleado();  // Llama a la función para enviar el formulario
    });
});


