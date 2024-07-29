from customtkinter import *
import customtkinter
from tkinter import messagebox, ttk
import tkinter as tk
import subprocess
import requests
import threading
import re

set_appearance_mode("light")

# Establecer el tema de colores y la fuente
COLOR_FONDO = "#020936"
COLOR_TEXTO = "#FFFFFF"
COLOR_BOTONES = "#071A99"
FUENTE_TEXTO = ("Arial", 12)

# Función para mostrar la barra de progreso
def barra_de_carga(parent):
    global lbl_general, progressbar, lbl

    lbl_general = tk.LabelFrame(parent, bg="white", bd=2)
    lbl_general.place(relx=0.5, rely=0.5, anchor='center', width=300, height=100)

    progressbar = ttk.Progressbar(lbl_general, mode="indeterminate")
    progressbar.start(10)
    progressbar.pack(pady=20)

    lbl = tk.Label(lbl_general, text="Cargando...")
    lbl.config(bg="white", fg="black", borderwidth=2)
    lbl.pack()

# Función para ejecutar tareas en segundo plano
def run_in_background(func, *args, **kwargs):
    threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()

# Función para instalar un paquete
def instalar_paquete():
    paquete = entrada_paquete.get()
    if not paquete:
        messagebox.showerror("Error", "Por favor, ingrese el nombre del paquete.")
        return
    
    barra_de_carga(frame_derecho)
    run_in_background(instalar_paquete_thread, paquete)

def instalar_paquete_thread(paquete):
    try:
        result = subprocess.run(['pip', 'install', paquete], capture_output=True, text=True, check=True)
        print(result.stdout)
        root.after(0, lambda: messagebox.showinfo("Instalación", f"El paquete '{paquete}' ha sido instalado."))
        root.after(0, actualizar_list_paquetes_instalados)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.lower()
        if "found existing installation" in error_message or "requirement already satisfied" in error_message:
            root.after(0, lambda: messagebox.showinfo("Instalación", f"{paquete} ya está instalado."))
        elif "no matching distribution found" in error_message:
            root.after(0, lambda: messagebox.showerror("Error", f"{paquete} no fue encontrado"))
        elif "invalid requirement" in error_message:
            root.after(0, lambda: messagebox.showerror("Error", f"Requisito inválido: {paquete}"))
        else:
            root.after(0, lambda: messagebox.showerror("Error", f"Error al instalar {paquete}: {e.stderr}"))
        print(e.stderr)
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para desinstalar un paquete
def desinstalar_paquete():
    paquete = entrada_paquete.get()
    if not paquete:
        messagebox.showerror("Error", "Por favor, ingrese el nombre del paquete.")
        return
    
    barra_de_carga(frame_derecho)
    run_in_background(desinstalar_paquete_thread, paquete)

def desinstalar_paquete_thread(paquete):
    try:
        result = subprocess.run(['pip', 'uninstall', '-y', paquete], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        print(output)
        if "Successfully uninstalled" in output:
            root.after(0, lambda: messagebox.showinfo("Desinstalación", f"El paquete '{paquete}' ha sido desinstalado."))
            root.after(0, actualizar_list_paquetes_instalados)
        elif "is not installed" in output:
            root.after(0, lambda: messagebox.showinfo("Desinstalación", f"El paquete '{paquete}' no está instalado."))
        else:
            root.after(0, lambda: messagebox.showinfo("Desinstalación", output))
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al desinstalar el paquete '{paquete}': {e.stderr}"))
        print(e.stderr)
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para actualizar la lista de paquetes instalados
def actualizar_list_paquetes_instalados():
    list_paquetes_instalados.delete(0, tk.END)
    for paquete in paquetes_predeterminados:
        list_paquetes_instalados.insert(tk.END, paquete)

# Función para instalar un paquete desde la lista
def instalar_paquete_lista(event):
    index = list_paquetes_instalados.curselection()
    if index:
        paquete = list_paquetes_instalados.get(index)
        entrada_paquete.delete(0, tk.END)
        entrada_paquete.insert(0, paquete)
        instalar_paquete()

# Función para actualizar la lista de mis paquetes instalados
def actualizar_mis_paquetes():
    barra_de_carga(frame_mis_paquetes_instalados)
    run_in_background(actualizar_mis_paquetes_thread)

def actualizar_mis_paquetes_thread():
    try:
        paquetes = subprocess.run(['pip', 'list', '--format=freeze'], capture_output=True, text=True, check=True)
        paquetes_list = paquetes.stdout.split('\n')
        root.after(0, lambda: mis_paquetes_instalados.delete(0, tk.END))
        for item in paquetes_list:
            if item:
                root.after(0, lambda i=item: mis_paquetes_instalados.insert(tk.END, i))
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al obtener la lista de paquetes: {e.stderr}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para exportar la lista de paquetes a un archivo
def exportar():
    barra_de_carga(frame_mis_paquetes_instalados)
    run_in_background(exportar_thread)

def exportar_thread():
    try:
        with open("requirements.txt", "w") as archivo:
            paquetes = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
            archivo.writelines(paquetes.stdout)
        root.after(0, lambda: messagebox.showinfo("Exportación", "Exportado exitosamente a requirements.txt"))
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al exportar: {str(e)}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para actualizar un paquete
def actualizar_paquete():
    paquete = entrada_paquete.get()
    if not paquete:
        messagebox.showerror("Error", "Por favor, ingrese el nombre del paquete.")
        return
    
    barra_de_carga(frame_derecho)
    run_in_background(actualizar_paquete_thread, paquete)

def actualizar_paquete_thread(paquete):
    try:
        result = subprocess.run(['pip', 'install', '--upgrade', paquete], capture_output=True, text=True, check=True)
        print(result.stdout)
        root.after(0, lambda: messagebox.showinfo("Actualización", f"El paquete '{paquete}' ha sido actualizado."))
        root.after(0, actualizar_list_paquetes_instalados)
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al actualizar el paquete '{paquete}': {e.stderr}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para buscar paquetes en PyPI
def buscar_paquetes():
    termino = entrada_busqueda.get()
    if termino:
        barra_de_carga(frame_busqueda)
        run_in_background(buscar_paquetes_thread, termino)

def buscar_paquetes_thread(termino):
    try:
        url = f"https://pypi.org/pypi/{termino}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            nombre_paquete = data["info"]["name"]
            version_paquete = data["info"]["version"]
            descripcion_paquete = data["info"]["summary"]
            root.after(0, lambda: resultado_busqueda.set(f"{nombre_paquete} ({version_paquete}): {descripcion_paquete}"))
        else:
            root.after(0, lambda: resultado_busqueda.set("Paquete no encontrado."))
    except Exception as e:
        root.after(0, lambda: resultado_busqueda.set(f"Error al buscar: {str(e)}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Función para actualizar las sugerencias en el Listbox
def actualizar_sugerencias(event):
    termino = entrada_busqueda.get().lower()
    sugerencias = [paquete for paquete in paquetes_predeterminados if termino in paquete.lower()]
    listbox_sugerencias.delete(0, tk.END)
    for sugerencia in sugerencias[:10]:  # Limitar a 10 sugerencias
        listbox_sugerencias.insert(tk.END, sugerencia)
    if sugerencias:
        listbox_sugerencias.place(relx=0.5, rely=0.3, anchor='n', width=200)
    else:
        listbox_sugerencias.place_forget()

# Función para completar el campo de entrada con la selección del Listbox
def completar_sugerencia(event):
    seleccion = listbox_sugerencias.curselection()
    if seleccion:
        entrada_busqueda.delete(0, tk.END)
        entrada_busqueda.insert(0, listbox_sugerencias.get(seleccion))
        listbox_sugerencias.place_forget()

# Configuración de la ventana principal
root = CTk()
root.title("Gestor de Paquetes pip")
root.configure(bg=COLOR_FONDO)
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Crear un ttk.Notebook
notebook_principal = ttk.Notebook(root)
notebook_principal.pack(fill='both', expand=True)

# Estilo para los frames
style = ttk.Style()
style.configure("TFrame", background=COLOR_FONDO)

# Pestaña para instalar/desinstalar
frame_derecho = ttk.Frame(notebook_principal, style="TFrame")
notebook_principal.add(frame_derecho, text="Instalar/Desinstalar")

# Etiquetas y entradas para el nombre del paquete
etiqueta = tk.Label(frame_derecho, text="Ingrese el nombre del paquete:", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO)
etiqueta.pack(pady=10)
entrada_paquete = CTkEntry(frame_derecho, font=FUENTE_TEXTO)
entrada_paquete.pack(pady=5)

# Crear botones para instalar, desinstalar y actualizar paquetes
boton_instalar = CTkButton(frame_derecho, text="Instalar", command=instalar_paquete)
boton_instalar.pack(pady=5)
boton_desinstalar = CTkButton(frame_derecho, text="Desinstalar", command=desinstalar_paquete)
boton_desinstalar.pack(pady=5)
boton_actualizar = CTkButton(frame_derecho, text="Actualizar", command=actualizar_paquete)
boton_actualizar.pack(pady=5)

# Pestaña para mostrar la lista de paquetes instalados
frame_lateral = ttk.Frame(notebook_principal, style="TFrame")
notebook_principal.add(frame_lateral, text="Paquetes Instalados")

# Crear otro ttk.Notebook para mostrar los paquetes instalados
notebook_secundario = ttk.Notebook(frame_lateral)
notebook_secundario.pack(fill='both', expand=True)

# Frame para mostrar los paquetes predeterminados
frame_paquetes_instalados = ttk.Frame(notebook_secundario, style="TFrame")
notebook_secundario.add(frame_paquetes_instalados, text="Instalar Paquetes")

# Listbox para mostrar paquetes instalados
list_paquetes_instalados = tk.Listbox(frame_paquetes_instalados, bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO, selectbackground=COLOR_BOTONES)
list_paquetes_instalados.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
list_paquetes_instalados.bind("<<ListboxSelect>>", instalar_paquete_lista)

# Frame para mostrar mis paquetes instalados
frame_mis_paquetes_instalados = ttk.Frame(notebook_secundario, style="TFrame")
notebook_secundario.add(frame_mis_paquetes_instalados, text="Mis Paquetes")

# Listbox para mostrar mis paquetes instalados
mis_paquetes_instalados = tk.Listbox(frame_mis_paquetes_instalados, bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO, selectbackground=COLOR_BOTONES)
mis_paquetes_instalados.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Botón para exportar la lista de paquetes instalados
boton_exportar = CTkButton(frame_mis_paquetes_instalados, text="Exportar", command=exportar)
boton_exportar.pack(pady=10)

# Botón para actualizar la lista de paquetes instalados
boton_actualizar_lista = CTkButton(frame_mis_paquetes_instalados, text="Actualizar Lista", command=actualizar_mis_paquetes)
boton_actualizar_lista.pack(pady=10)

# Pestaña para buscar paquetes en PyPI
frame_busqueda = ttk.Frame(notebook_principal, style="TFrame")
notebook_principal.add(frame_busqueda, text="Buscar en PyPI")

# Etiqueta y entrada para buscar en PyPI
etiqueta_busqueda = tk.Label(frame_busqueda, text="Buscar paquete en PyPI:", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO)
etiqueta_busqueda.pack(pady=10)
entrada_busqueda = CTkEntry(frame_busqueda, font=FUENTE_TEXTO)
entrada_busqueda.pack(pady=5)
entrada_busqueda.bind('<KeyRelease>', actualizar_sugerencias)
entrada_busqueda.bind('<FocusOut>', lambda e: root.after(100, listbox_sugerencias.place_forget))
entrada_busqueda.bind('<FocusIn>', actualizar_sugerencias)

# Listbox para mostrar sugerencias de búsqueda
listbox_sugerencias = tk.Listbox(frame_busqueda, bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_TEXTO, selectbackground=COLOR_BOTONES)
listbox_sugerencias.bind("<<ListboxSelect>>", completar_sugerencia)
listbox_sugerencias.place_forget()

# Botón para buscar en PyPI
boton_buscar = CTkButton(frame_busqueda, text="Buscar", command=buscar_paquetes)
boton_buscar.pack(pady=10)

# Etiqueta para mostrar resultados de búsqueda
resultado_busqueda = tk.StringVar()
resultado_label = tk.Label(frame_busqueda, textvariable=resultado_busqueda, background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO, wraplength=400)
resultado_label.pack(pady=10)

# Lista de paquetes predeterminados
paquetes_predeterminados = [
    "absl-py", "aiohttp", "alabaster", "altair", "argparse", "asgiref", "astropy",
    "asyncio", "attrs", "beautifulsoup4", "bokeh", "boto3", "bottle", "celery",
    "certifi", "chainer", "chardet", "click", "cloudpickle", "Cython", "dash",
    "dask", "dataclasses", "decorator", "dill", "Django", "Flask", "gensim",
    "geopandas", "google-auth", "google-cloud-storage", "grpcio", "gunicorn",
    "h5py", "h2o", "idna", "imageio", "ipython", "ipywidgets", "jedi", "Jinja2",
    "joblib", "jsonschema", "Keras", "kiwisolver", "kornia", "lightgbm", "lxml",
    "matplotlib", "mistune", "mkl", "mxnet", "networkx", "nltk", "notebook",
    "numba", "numpy", "nvidia-ml-py3", "opencv-python", "openpyxl", "optuna",
    "pandas", "Pillow", "pip", "plotly", "pluggy", "protobuf", "psutil",
    "psycopg2", "pytest", "pytz", "PyYAML", "requests", "retrying",
    "scikit-image", "scikit-learn", "scipy", "seaborn", "selenium", "sklearn",
    "spacy", "SQLAlchemy", "statsmodels", "sympy", "tabulate", "tbb", "tensorboard",
    "tensorflow", "termcolor", "tornado", "tqdm", "twisted", "typing-extensions",
    "urllib3", "virtualenv", "Werkzeug", "wordcloud", "wxPython", "xgboost",
    "xlrd", "XlsxWriter", "xlwt", "yarl", "bcrypt", "blinker", "bson", "cairocffi",
    "cryptography", "cycler", "dataclasses-json", "docopt", "ecdsa", "email-validator",
    "filelock", "gensim", "google-api-python-client", "greenlet", "httpx", "hyperopt",
    "iso8601", "json5", "loguru", "matplotlib-venn", "mypy", "nltk", "openai", "orjson",
    "passlib", "pillow", "pipenv", "poetry", "praw", "pybind11", "pydantic", "pygments",
    "pyjwt", "pymongo", "pyparsing", "pyrsistent", "python-dateutil", "python-dotenv",
    "pytube", "pyyaml", "regex", "rich", "scikit-optimize", "setuptools", "shap",
    "six", "snorkel", "soundfile", "sqlparse", "starlette", "subprocess", "textblob",
    "toml", "transformers", "twilio", "ujson", "uvicorn", "watchdog", "websockets",
    "xlutils", "yfinance", "youtube-dl", "pyautogui"
]


# Función para verificar actualizaciones disponibles
def verificar_actualizaciones():
    barra_de_carga(frame_mis_paquetes_instalados)
    run_in_background(verificar_actualizaciones_thread)

def verificar_actualizaciones_thread():
    try:
        result = subprocess.run(['pip', 'list', '--outdated', '--format=json'], capture_output=True, text=True, check=True)
        paquetes_desactualizados = json.loads(result.stdout)
        if paquetes_desactualizados:
            mensaje = "Paquetes con actualizaciones disponibles:\n\n"
            for paquete in paquetes_desactualizados:
                mensaje += f"{paquete['name']} (installed: {paquete['version']}, latest: {paquete['latest_version']})\n"
            root.after(0, lambda: messagebox.showinfo("Actualizaciones disponibles", mensaje))
        else:
            root.after(0, lambda: messagebox.showinfo("Actualizaciones", "Todos los paquetes están actualizados."))
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al verificar actualizaciones: {e.stderr}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Botón para verificar actualizaciones
boton_verificar_actualizaciones = CTkButton(frame_mis_paquetes_instalados, text="Verificar Actualizaciones", command=verificar_actualizaciones)
boton_verificar_actualizaciones.pack(pady=10)

# Función para instalar desde requirements.txt
def instalar_desde_requirements():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        barra_de_carga(frame_derecho)
        run_in_background(instalar_desde_requirements_thread, filename)

def instalar_desde_requirements_thread(filename):
    try:
        result = subprocess.run(['pip', 'install', '-r', filename], capture_output=True, text=True, check=True)
        root.after(0, lambda: messagebox.showinfo("Instalación", "Paquetes instalados correctamente desde requirements.txt"))
        root.after(0, actualizar_mis_paquetes)
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al instalar desde requirements.txt: {e.stderr}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Botón para instalar desde requirements.txt
boton_instalar_requirements = CTkButton(frame_derecho, text="Instalar desde requirements.txt", command=instalar_desde_requirements)
boton_instalar_requirements.pack(pady=10)

# Función para mostrar información detallada del paquete
def mostrar_info_paquete(event):
    seleccion = mis_paquetes_instalados.curselection()
    if seleccion:
        paquete = mis_paquetes_instalados.get(seleccion)
        nombre_paquete = paquete.split('==')[0]
        barra_de_carga(frame_mis_paquetes_instalados)
        run_in_background(mostrar_info_paquete_thread, nombre_paquete)

def mostrar_info_paquete_thread(nombre_paquete):
    try:
        result = subprocess.run(['pip', 'show', nombre_paquete], capture_output=True, text=True, check=True)
        info = result.stdout
        root.after(0, lambda: messagebox.showinfo(f"Información de {nombre_paquete}", info))
    except subprocess.CalledProcessError as e:
        root.after(0, lambda: messagebox.showerror("Error", f"Error al obtener información del paquete: {e.stderr}"))
    finally:
        root.after(0, lambda: lbl_general.destroy())

# Vincular el evento de doble clic en la lista de paquetes instalados
mis_paquetes_instalados.bind('<Double-1>', mostrar_info_paquete)

# Actualizar la lista de paquetes y mis paquetes al iniciar la aplicación
actualizar_list_paquetes_instalados()
actualizar_mis_paquetes()

# Iniciar la aplicación
root.mainloop()
