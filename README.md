# Gestor de Paquetes Tkinter para Windows

Este es un gestor de paquetes desarrollado en Python utilizando la biblioteca Tkinter para la interfaz gráfica. Permite instalar, desinstalar, actualizar y buscar paquetes de Python desde PyPI (Python Package Index) de manera fácil y rápida, especialmente diseñado para usuarios de Windows.

## Características

- Interfaz gráfica amigable y fácil de usar.
- Instalación, desinstalación y actualización de paquetes.
- Búsqueda de paquetes en PyPI.
- Exportación de la lista de paquetes instalados a un archivo de texto.

## Requisitos previos

1. **Python 3.x**: Si no tienes Python instalado, descárgalo e instálalo desde [python.org](https://www.python.org/downloads/windows/). Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

2. **Git** (opcional): Si prefieres clonar el repositorio. Descárgalo e instálalo desde [git-scm.com](https://git-scm.com/download/win).

## Instalación

### Opción 1: Descarga directa (recomendado para principiantes)

1. Ve a la página del repositorio: https://github.com/markbus-ai/gui-pip
2. Haz clic en el botón verde "Code" y selecciona "Download ZIP".
3. Descomprime el archivo ZIP en la ubicación que prefieras.

### Opción 2: Clonar con Git

Si tienes Git instalado, abre el Command Prompt y ejecuta:

```bash
git clone https://github.com/markbus-ai/gui-pip
cd gui-pip
```

## Configuración

1. Abre el Command Prompt (puedes buscarlo en el menú de inicio).
2. Navega hasta el directorio donde descargaste o clonaste el proyecto:
   ```
   cd ruta\al\directorio\gui-pip
   ```
3. Instala las dependencias necesarias:
   ```
   pip install customtkinter
   ```

## Uso

1. En el mismo Command Prompt, ejecuta la aplicación:
   ```
   python gui.py
   ```
2. Se abrirá la interfaz gráfica del Gestor de Paquetes Tkinter.

## Guía rápida

- **Instalar un paquete**: Escribe el nombre del paquete en el campo de texto y haz clic en "Instalar".
- **Desinstalar un paquete**: Escribe el nombre del paquete y haz clic en "Desinstalar".
- **Buscar un paquete**: Usa la pestaña "Buscar en PyPI" para encontrar información sobre paquetes.
- **Exportar lista de paquetes**: En la pestaña "Mis Paquetes", usa el botón "Exportar" para guardar la lista de paquetes instalados.

## Solución de problemas

- Si recibes un error de "python no reconocido como comando", asegúrate de que Python esté correctamente añadido a tu PATH de Windows.
- Si hay problemas con la instalación de `customtkinter`, intenta actualizar pip:
  ```
  python -m pip install --upgrade pip
  ```
  Y luego vuelve a intentar instalar `customtkinter`.

## Contribuciones

Si encuentras algún error o tienes alguna sugerencia para mejorar este proyecto, no dudes en abrir un issue o enviar un pull request en GitHub. ¡Todas las contribuciones son bienvenidas!

## Autor

Este proyecto fue creado por Markbusking.

## Licencia

Este proyecto está bajo la Licencia MIT.
