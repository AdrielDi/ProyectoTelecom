using System;
using System.Diagnostics;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace AppMonitor
{
    class Program
    {
        // Cambia la dirección IP y el puerto según tu configuración
        private const string DjangoServerUrl = "http://127.0.0.1:8000";

        static async Task Main(string[] args)
        {
            while (true)
            {
                // Obtenemos la aplicación activa
                var activeApp = GetActiveApplication();
                Console.WriteLine($"Aplicación activa: {activeApp}");

                try
                {
                    // Obtener el token CSRF del servidor Django
                    var csrfToken = await GetCSRFToken();

                    // Enviar los datos al servidor Django
                    await SendDataToDjango(activeApp, csrfToken);
                    Console.WriteLine("Datos enviados con éxito al servidor Django.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error al enviar los datos al servidor Django: {ex.Message}");
                }

                // Pausa para evitar una alta carga de CPU
                System.Threading.Thread.Sleep(5000); // Cambia el valor a tu preferencia (en milisegundos)
            }
        }

        static string GetActiveApplication()
        {
            IntPtr handle = GetForegroundWindow();
            int processId;
            GetWindowThreadProcessId(handle, out processId);
            Process process = Process.GetProcessById(processId);
            return process.ProcessName;
        }

        static async Task<string> GetCSRFToken()
        {
            using (var httpClient = new HttpClient())
            {
                var response = await httpClient.GetAsync($"{DjangoServerUrl}/get_csrf_token/"); // Utiliza la nueva URL

                if (response.IsSuccessStatusCode)
                {
                    var csrfToken = await response.Content.ReadAsStringAsync();
                    return csrfToken;
                }
                else
                {
                    throw new Exception("No se pudo obtener el token CSRF.");
                }
            }
        }

        static async Task SendDataToDjango(string activeApp, string csrfToken)
        {
            using (var httpClient = new HttpClient())
            {
                var postData = new
                {
                    active_app = activeApp,
                    activity_description = "Descripción de la actividad"
                };

                var content = new StringContent(Newtonsoft.Json.JsonConvert.SerializeObject(postData), Encoding.UTF8, "application/json");

                // Incluye el token CSRF en el encabezado de la solicitud
                httpClient.DefaultRequestHeaders.Add("X-CSRFToken", csrfToken);

                try
                {
                    var response = await httpClient.PostAsync($"{DjangoServerUrl}/capture_active_app/", content);

                    if (!response.IsSuccessStatusCode)
                    {
                        throw new Exception($"Código de estado HTTP: {response.StatusCode}");
                    }
                }
                catch (Exception ex)
                {
                    throw new Exception($"Error al enviar la solicitud HTTP: {ex.Message}");
                }
            }
        }

        [System.Runtime.InteropServices.DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        [System.Runtime.InteropServices.DllImport("user32.dll")]
        private static extern int GetWindowThreadProcessId(IntPtr hWnd, out int ProcessId);
    }
}
