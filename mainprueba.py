try:
    from Principal import interfaz  # Importamos la clase de la interfaz
except ImportError as e:
    print(f"Error importing interfaz: {e}")
    exit(1)

if __name__ == "__main__":
    try:
        app = interfaz()  # Creamos la instancia de la interfaz
        app.mainloop()  # Iniciamos el bucle de Tkinter
    except Exception as e:
        print(f"Error running the app: {e}")
        exit(1)
