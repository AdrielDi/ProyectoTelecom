// Convierte los datos recibidos del view para adaptarlos a una etiqueta de HTML, La cual está en el template de Activity_Template.HTML
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

    setInterval(updateActiveAppData, 10000); // Tiempo en milisegundos
});