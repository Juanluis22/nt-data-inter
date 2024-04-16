def obtener_nombre():
    nombre = input("Por favor, ingresa tu nombre: ")
    return nombre

def imprimir_mensaje(nombre):
    print("¡Hola, {}! Bienvenido al programa.".format(nombre))

def main():
    nombre = obtener_nombre()
    imprimir_mensaje(nombre)

if __name__ == "__main__":
    main()