import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import requests

# Establecer el tema de colores y la fuente
COLOR_FONDO = "#020936"
COLOR_TEXTO = "#FFFFFF"
COLOR_BOTONES = "#071A99"
FUENTE_TEXTO = ("Arial", 12)

# Función para mostrar la barra de progreso
def barra_de_carga(parent):
    global lbl_general, progressbar, lbl

    # Crear un contenedor para la barra de progreso y el texto
    lbl_general = tk.LabelFrame(parent, bg="white", bd=2)
    lbl_general.place(relx=0.5, rely=0.5, anchor='center', width=300, height=100)

    # Crear y configurar la barra de progreso
    progressbar = ttk.Progressbar(lbl_general, mode="indeterminate")
    progressbar.start(10)
    progressbar.pack(pady=20)  # Empaquetar con un margen superior

    # Crear y configurar el texto "Cargando..."
    lbl = tk.Label(lbl_general, text="Cargando...")
    lbl.config(bg="white", fg="black", borderwidth=2)
    lbl.pack()  # Empaquetar sin margen

# Función para instalar un paquete
def instalar_paquete():
    barra_de_carga(frame_derecho)
    paquete = entrada_paquete.get()
    try:
        # Ejecutar el comando pip para instalar el paquete
        result = subprocess.run(['pip', 'install', paquete], capture_output=True, text=True, check=True)
        print(result.stdout)  # Imprimir la salida estándar
        messagebox.showinfo("Instalación", f"El paquete '{paquete}' ha sido instalado.")
        actualizar_list_paquetes_instalados()
    except subprocess.CalledProcessError as e:
        if "Requirement already satisfied" in e.stderr:
            messagebox.showerror(message=f"{paquete} ya está instalado.")
        elif "No matching distribution found" in e.stderr:
            messagebox.showerror(message=f"{paquete} no fue encontrado")
        elif "Invalid requirement" in e.stderr:
            messagebox.showerror(message=e.stderr)
        print(e.stderr)  # Imprimir la salida de error
    lbl_general.destroy()

# Función para desinstalar un paquete
def desinstalar_paquete():
    barra_de_carga(frame_derecho)
    paquete = entrada_paquete.get()
    try:
        with subprocess.Popen(['pip', 'uninstall', paquete], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            output, error = proc.communicate(input='y\n', timeout=10)
            output = output.strip()  # Eliminar espacios en blanco adicionales
            error = error.strip()
            print(output)  # Imprimir la salida estándar
            if "Successfully uninstalled" in output:
                messagebox.showinfo("Desinstalación", f"El paquete '{paquete}' ha sido desinstalado.")
                actualizar_list_paquetes_instalados()
            elif "is not installed" in output:
                messagebox.showerror("Desinstalación", f"El paquete '{paquete}' no está instalado.")
            elif "Found existing" and "Can't uninstall" in output:
                messagebox.showerror("Error", f"Error al desinstalar el paquete debido a falta de permisos paquete:'{paquete}': {error}")
            elif error:
                messagebox.showerror("Error", f"Error al desinstalar el paquete '{paquete}': {error}")
    except subprocess.CalledProcessError as e:
        print(e.stderr)
    lbl_general.destroy()

# Función para actualizar la lista de paquetes instalados
def actualizar_list_paquetes_instalados():
    list_paquetes_instalados.delete(0, tk.END)
    for paquete in paquetes_predeterminados:
        list_paquetes_instalados.insert(tk.END, paquete)

# Función para instalar un paquete desde la lista
def instalar_paquete_lista(event):
    barra_de_carga(frame_paquetes_instalados)
    index = list_paquetes_instalados.curselection()
    if index:
        paquete = list_paquetes_instalados.get(index)
        try:
            result = subprocess.run(['pip', 'install', paquete], capture_output=True, text=True, check=True)
            print(result.stdout)
            messagebox.showinfo("Instalación", f"El paquete '{paquete}' ha sido instalado.")
            actualizar_list_paquetes_instalados()
        except subprocess.CalledProcessError as e:
            if "Requirement already satisfied" in e.stderr:
                messagebox.showerror(message=f"{paquete} ya está instalado.")
            elif "No matching distribution found" in e.stderr:
                messagebox.showerror(message=f"{paquete} no fue encontrado")
            elif "Invalid requirement" in e.stderr:
                messagebox.showerror(message=e.stderr)
            print(e.stderr)
    lbl_general.destroy()

# Función para actualizar la lista de mis paquetes instalados
def actualizar_mis_paquetes():
    paquetes = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
    paquetes_list = paquetes.stdout.split('\n')
    mis_paquetes_instalados.delete(0, tk.END)
    for item in paquetes_list:
        mis_paquetes_instalados.insert(tk.END, item)

# Función para exportar la lista de paquetes a un archivo
def exportar():
    with open("requeriments.txt", "w") as archivo:
        paquetes = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        archivo.writelines(paquetes.stdout)
        messagebox.showinfo(message="Exportado exitosamente")

# Función para actualizar un paquete
def actualizar_paquete():
    barra_de_carga(frame_derecho)
    paquete = entrada_paquete.get()
    try:
        result = subprocess.run(['pip', 'install', '--upgrade', paquete], capture_output=True, text=True, check=True)
        print(result.stdout)
        messagebox.showinfo("Actualización", f"El paquete '{paquete}' ha sido actualizado.")
        actualizar_list_paquetes_instalados()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al actualizar el paquete '{paquete}': {e.stderr}")
    lbl_general.destroy()

# Función para buscar paquetes en PyPI
def buscar_paquetes():
    termino = entrada_busqueda.get()
    if termino:
        url = f"https://pypi.org/pypi/{termino}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            nombre_paquete = data["info"]["name"]
            version_paquete = data["info"]["version"]
            descripcion_paquete = data["info"]["summary"]
            resultado_busqueda.set(f"{nombre_paquete} ({version_paquete}): {descripcion_paquete}")
        else:
            resultado_busqueda.set("Paquete no encontrado.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Paquetes Tkinter")
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
etiqueta = ttk.Label(frame_derecho, text="Ingrese el nombre del paquete:", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO)
etiqueta.pack(pady=10)
entrada_paquete = ttk.Entry(frame_derecho, font=FUENTE_TEXTO)
entrada_paquete.pack(pady=5)

# Crear botones para instalar, desinstalar y actualizar paquetes
boton_instalar = ttk.Button(frame_derecho, text="Instalar", command=instalar_paquete)
boton_instalar.pack(pady=5)
boton_desinstalar = ttk.Button(frame_derecho, text="Desinstalar", command=desinstalar_paquete)
boton_desinstalar.pack(pady=5)
boton_actualizar = ttk.Button(frame_derecho, text="Actualizar", command=actualizar_paquete)
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
boton_exportar = ttk.Button(frame_mis_paquetes_instalados, text="Exportar", command=exportar)
boton_exportar.pack(pady=10)

# Pestaña para buscar paquetes en PyPI
frame_busqueda = ttk.Frame(notebook_principal, style="TFrame")
notebook_principal.add(frame_busqueda, text="Buscar en PyPI")

# Etiqueta y entrada para buscar en PyPI
etiqueta_busqueda = ttk.Label(frame_busqueda, text="Buscar paquete en PyPI:", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO)
etiqueta_busqueda.pack(pady=10)
entrada_busqueda = ttk.Entry(frame_busqueda, font=FUENTE_TEXTO)
entrada_busqueda.pack(pady=5)
boton_buscar = ttk.Button(frame_busqueda, text="Buscar", command=buscar_paquetes)
boton_buscar.pack(pady=10)

# Etiqueta para mostrar resultados de búsqueda
resultado_busqueda = tk.StringVar()
resultado_label = ttk.Label(frame_busqueda, textvariable=resultado_busqueda, background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TEXTO, wraplength=400)
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
    "xlrd", "XlsxWriter", "xlwt", "yarl"
]

# Actualizar la lista de paquetes y mis paquetes al iniciar la aplicación
actualizar_list_paquetes_instalados()
actualizar_mis_paquetes()
root.mainloop()
