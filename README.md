# :syringe: Proyecto de Gestión de Información sobre Vacunación en Panamá - Fronted

![Imagen logo del proyecto](https://github.com/Kingg22/api-vacunas-panama/blob/6af77570fccb3737547a1065f8f4d25316c896c8/src/main/resources/images/icon.png)

Este es el repositorio **fronted** para el proyecto, el cual tiene como objetivo facilitar la gestión y seguimiento de 
vacunas en diversas sedes y con múltiples usuarios. Esta aplicación permite la interacción con el backend para realizar operaciones relacionadas con la administración de
pacientes, vacunas y demás recursos asociados.

## Funcionalidades Clave
- Visualización y gestión de datos de pacientes y vacunas.
- UI para la administración de inventarios de vacunas en diferentes sedes.
- Soporte para la creación de usuarios.
- Integración con el backend para realizar consultas en tiempo real sobre la disponibilidad de dosis, vacunas y más.

Para más información sobre el proyecto completo y su funcionamiento, consulta el [repositorio principal](https://github.com/Kingg22/desktopapp-vacunas-panama/tree/refactor/api)

## :hammer_and_wrench:Tecnologías Utilizadas
- [Python](https://www.python.org/) - Lenguaje de programación para el fronted.
- [Flet](https://flet.dev/) - Framework para construir aplicaciones multi plataforma (Web, Desktop and mobile) en Python.
- [Pydantic](https://docs.pydantic.dev/latest/) - Librería para hacer validaciones de datos previas a interactuar con el backend.
- [Httpx](https://www.python-httpx.org/) - Cliente HTTP para Python.

Lista completa de dependencias en requirements.txt

## :wrench: Clonación y configuración del repositorio
Sigue estos pasos para clonar el repositorio:
> [!NOTE]
> Requiere [Python](https://www.python.org/downloads/) instalado. Para las funcionalidades con el backend debe estar funcionando
> para que el fronted se conecte correctamente. Puedes seguir las instrucciones de instalación y configuración del backend en [este enlace](https://github.com/Kingg22/desktopapp-vacunas-panama/blob/refactor/api/README.md#wrench-clonaci%C3%B3n-y-configuraci%C3%B3n-del-repositorio).

1. Clona este repositorio
    ```bash
    git clone https://github.com/patrickvillarroel/flet-vacunas-panama
    ```
2. Crear un [entorno virtual](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) para el proyecto
    ```bash
   python -m venv .venv
    ```
   Activar el entorno virtual
   
   Para Windows:
   ```bash
   .venv\Scripts\activate
    ```
   Otros SO:
   ```bash
   .venv/bin/activate
    ```
3. Instala las dependencias
    ```bash
    pip install -r requirements.txt
    ```
4. Crear archivo .env con:
   ```dotenv
    BASE_URL=link a la api
   ```
5. Iniciar el programa

   Desktop app:
   ```bash
   flet run
   ```
   Web app:
   ```bash
   flet run --web --port 8000 main.py
   ```
   iOS: https://flet.dev/docs/getting-started/testing-on-ios

   Android: https://flet.dev/docs/getting-started/testing-on-android

   Publish: https://flet.dev/docs/publish