class Omnibus:
    def __init__(self, chapa, km_recorridos, km_max, disponible, estado, capacidad):
        self.chapa = chapa
        self.km_recorridos = km_recorridos
        self.km_max = km_max
        self.disponible = disponible
        self.estado = estado
        self.capacidad = capacidad

    def __str__(self):
        return f"Ómnibus {self.chapa}: {self.km_recorridos} km recorridos, {self.km_max} km max, {self.estado}, Capacidad: {self.capacidad}"

class Chofer:
    def __init__(self, calificacion, identificacion, anios_experiencia):
        self.calificacion = calificacion
        self.identificacion = identificacion
        self.anios_experiencia = anios_experiencia

    def __str__(self):
        return f"Chofer {self.identificacion}: Calificación {self.calificacion}, Años de experiencia: {self.anios_experiencia}"

class Viaje:
    def __init__(self, codigo, km_recorrer, costo_estimado, chofer_id, tipo_viaje, provincia=None, especial=False, paradas=None):
        self.codigo = codigo
        self.km_recorrer = km_recorrer
        self.costo_estimado = costo_estimado
        self.chofer_id = chofer_id
        self.tipo_viaje = tipo_viaje
        self.provincia = provincia
        self.especial = especial
        self.paradas = paradas
        self.omnibus = None  # Referencia al ómnibus asignado al viaje

    def __str__(self):
        return f"Viaje {self.codigo}: {self.km_recorrer} km, Costo estimado: {self.costo_estimado}, Chofer: {self.chofer_id}, Tipo: {self.tipo_viaje}"

class Terminal:
    def __init__(self):
        self.omnibuses = []
        self.choferes = []
        self.viajes = []
        self.provincias = []

    def agregar_omnibus(self, omnibus):
        self.omnibuses.append(omnibus)

    def actualizar_omnibus(self, chapa, nuevo_omnibus):
        for i in range(len(self.omnibuses)):
            if self.omnibuses[i].chapa == chapa:
                self.omnibuses[i] = nuevo_omnibus
                return
        print("Ómnibus no encontrado.")

    def eliminar_omnibus(self, chapa):
        self.omnibuses = [o for o in self.omnibuses if o.chapa != chapa]

    def listar_omnibuses_por_capacidad(self):
        return sorted(self.omnibuses, key=lambda o: o.capacidad)

    def agregar_viaje(self, viaje):
        # Asignar un ómnibus al viaje si hay disponibles
        for omnibus in self.omnibuses:
            if omnibus.disponible:
                viaje.omnibus = omnibus
                omnibus.disponible = False  # Marcar el ómnibus como no disponible
                break
        self.viajes.append(viaje)

    def obtener_viajes_interprovinciales_especiales(self):
        return [v for v in self.viajes if v.tipo_viaje == 'interprovincial' and v.provincia == 'Camagüey' and v.especial]

    def cantidad_omnibuses_no_disponibles_malos(self):
        return sum(1 for o in self.omnibuses if not o.disponible and o.estado == 'malo')

    def listar_choferes_por_experiencia(self):
        return sorted(self.choferes, key=lambda c: c.anios_experiencia, reverse=True)

    def listar_omnibuses_km_bajo_y_calificacion(self, calificacion):
        return [o for o in self.omnibuses if (o.km_recorridos < o.km_max / 2) and (o in [c.omnibus for c in self.choferes if c.calificacion == calificacion])]

    def calcular_recaudacion_viaje(self, viaje):
        if viaje.omnibus is None:
            print("El viaje no tiene un ómnibus asignado.")
            return None
        costo = viaje.costo_estimado * viaje.omnibus.capacidad - viaje.km_recorrer * 1.5
        if viaje.tipo_viaje == 'interprovincial':
            if viaje.especial:
                costo -= 100
        return costo

    def mostrar_omnibuses(self):
        print("Listado de Ómnibus:")
        for omnibus in self.omnibuses:
            print(omnibus)

    def mostrar_choferes(self):
        print("Listado de Choferes:")
        for chofer in self.choferes:
            print(chofer)

    def mostrar_viajes(self):
        print("Listado de Viajes:")
        for viaje in self.viajes:
            print(viaje)

def menu_principal():
    terminal = Terminal()

    while True:
        print("\nMenú Principal:")
        print("1. Agregar ómnibus")
        print("2. Actualizar ómnibus")
        print("3. Eliminar ómnibus")
        print("4. Agregar chofer")
        print("5. Agregar viaje")
        print("6. Listar ómnibus por capacidad")
        print("7. Listar viajes interprovinciales especiales a Camagüey")
        print("8. Cantidad de ómnibus no disponibles y malos")
        print("9. Listar choferes por experiencia")
        print("10. Listar ómnibus con km bajo y calificación de chofer")
        print("11. Calcular recaudación de un viaje")
        print("12. Mostrar todos los ómnibus")
        print("13. Mostrar todos los choferes")
        print("14. Mostrar todos los viajes")
        print("15. Salir")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            chapa = input("Ingrese la chapa del ómnibus: ")
            km_recorridos = int(input("Ingrese los kilómetros recorridos: "))
            km_max = int(input("Ingrese los kilómetros máximos: "))
            disponible = input("¿Está disponible? (True/False): ").lower() == "true"
            estado = input("Ingrese el estado (Bueno/Regular/Malo): ")
            capacidad = int(input("Ingrese la capacidad: "))
            omnibus = Omnibus(chapa, km_recorridos, km_max, disponible, estado, capacidad)
            terminal.agregar_omnibus(omnibus)
            print("Ómnibus agregado exitosamente.")

        elif opcion == "2":
            chapa = input("Ingrese la chapa del ómnibus a actualizar: ")
            km_recorridos = int(input("Ingrese los nuevos kilómetros recorridos: "))
            km_max = int(input("Ingrese los nuevos kilómetros máximos: "))
            disponible = input("¿Está disponible? (True/False): ").lower() == "true"
            estado = input("Ingrese el nuevo estado (Bueno/Regular/Malo): ")
            capacidad = int(input("Ingrese la nueva capacidad: "))
            nuevo_omnibus = Omnibus(chapa, km_recorridos, km_max, disponible, estado, capacidad)
            terminal.actualizar_omnibus(chapa, nuevo_omnibus)
            print("Ómnibus actualizado exitosamente.")

        elif opcion == "3":
            chapa = input("Ingrese la chapa del ómnibus a eliminar: ")
            terminal.eliminar_omnibus(chapa)
            print("Ómnibus eliminado exitosamente.")

        elif opcion == "4":
            calificacion = input("Ingrese la calificación del chofer (A/B/C): ")
            identificacion = input("Ingrese la identificación del chofer: ")
            anios_experiencia = int(input("Ingrese los años de experiencia del chofer: "))
            chofer = Chofer(calificacion, identificacion, anios_experiencia)
            terminal.choferes.append(chofer)
            print("Chofer agregado exitosamente.")

        elif opcion == "5":
            codigo = input("Ingrese el código del viaje: ")
            km_recorrer = int(input("Ingrese los kilómetros a recorrer: "))
            costo_estimado = float(input("Ingrese el costo estimado por pasajero: "))
            chofer_id = input("Ingrese la identificación del chofer: ")
            tipo_viaje = input("Ingrese el tipo de viaje (intermunicipal/interprovincial): ")
            if tipo_viaje == "interprovincial":
                provincia = input("Ingrese la provincia de destino: ")
                especial = input("¿Es un viaje especial? (True/False): ").lower() == "true"
                viaje = Viaje(codigo, km_recorrer, costo_estimado, chofer_id, tipo_viaje, provincia, especial)
            else:
                paradas = int(input("Ingrese la cantidad de paradas intermedias: "))
                viaje = Viaje(codigo, km_recorrer, costo_estimado, chofer_id, tipo_viaje, paradas=paradas)
            terminal.agregar_viaje(viaje)
            print("Viaje agregado exitosamente.")

        elif opcion == "6":
            print("Listado de ómnibus por capacidad:")
            for omnibus in terminal.listar_omnibuses_por_capacidad():
                print(f"Chapa: {omnibus.chapa}, Capacidad: {omnibus.capacidad}")

        elif opcion == "7":
            print("Ómnibus en viajes interprovinciales especiales a Camagüey:")
            for viaje in terminal.obtener_viajes_interprovinciales_especiales():
                print(f"Código: {viaje.codigo}, Chofer ID: {viaje.chofer_id}")

        elif opcion == "8":
            cantidad = terminal.cantidad_omnibuses_no_disponibles_malos()
            print(f"Cantidad de ómnibus no disponibles y malos: {cantidad}")

        elif opcion == "9":
            print("Listado de choferes por experiencia:")
            for chofer in terminal.listar_choferes_por_experiencia():
                print(f"Identificación: {chofer.identificacion}, Años de experiencia: {chofer.anios_experiencia}")

        elif opcion == "10":
            calificacion = input("Ingrese la calificación de los choferes (A/B/C): ")
            omnibuses = terminal.listar_omnibuses_km_bajo_y_calificacion(calificacion)
            print("Ómnibus con km bajo y calificación de chofer:")
            for omnibus in omnibuses:
                print(f"Chapa: {omnibus.chapa}, Kilómetros recorridos: {omnibus.km_recorridos}")

        elif opcion == "11":
            codigo_viaje = input("Ingrese el código del viaje: ")
            viaje_encontrado = next((v for v in terminal.viajes if v.codigo == codigo_viaje), None)
            if viaje_encontrado:
                recaudacion = terminal.calcular_recaudacion_viaje(viaje_encontrado)
                if recaudacion is not None:
                    print(f"La recaudación del viaje {codigo_viaje} es: {recaudacion}")
            else:
                print("No se encontró el viaje especificado.")

        elif opcion == "12":
            terminal.mostrar_omnibuses()

        elif opcion == "13":
            terminal.mostrar_choferes()

        elif opcion == "14":
            terminal.mostrar_viajes()

        elif opcion == "15":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Por favor, intente de nuevo.")

# Pruebas para verificar el correcto funcionamiento del sistema
def pruebas_terminal():
    # Crear instancia de la terminal
    terminal = Terminal()

    # Agregar ómnibus de prueba
    omnibus1 = Omnibus('ABC123', 20000, 50000, True, 'Bueno', 50)
    omni2 = Omnibus('DEF456', 15000, 30000, False, 'Malo', 40)
    terminal.agregar_omnibus(omnibus1)
    terminal.agregar_omnibus(omni2)

    # Agregar choferes
    chofer1 = Chofer('A', 'CH1', 5)
    chofer2 = Chofer('B', 'CH2', 10)
    terminal.choferes.append(chofer1)
    terminal.choferes.append(chofer2)

    # Agregar viajes
    viaje1 = Viaje('V001', 300, 20, 'CH1', 'intermunicipal')
    viaje2 = Viaje('V002', 250, 30, 'CH2', 'interprovincial', 'Camagüey', True)
    terminal.agregar_viaje(viaje1)
    terminal.agregar_viaje(viaje2)

    # Probar las funcionalidades
    print('Listado de ómnibus por capacidad:')
    for omnibus in terminal.listar_omnibuses_por_capacidad():
        print(omnibus.chapa)

    print('\nCantidad de ómnibus no disponibles y malos:', terminal.cantidad_omnibuses_no_disponibles_malos())

    print('\nÓmnibus en viajes interprovinciales especiales a Camagüey:')
    for viaje in terminal.obtener_viajes_interprovinciales_especiales():
        print(viaje.codigo, viaje.chofer_id)

    print('\nListado de choferes por experiencia:')
    for chofer in terminal.listar_choferes_por_experiencia():
        print(chofer.identificacion, chofer.anios_experiencia)

    # Realizar pruebas de recaudación
    recaudacion = terminal.calcular_recaudacion_viaje(viaje2)
    if recaudacion is not None:
        print('\nRecaudación del viaje2:', recaudacion)

# Ejecución de pruebas
pruebas_terminal()

# Ejecución del menú principal
menu_principal()