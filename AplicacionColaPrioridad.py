import os
import time
import uuid

#**********************************************
# SISTEMA DE  PRIORIDAD HEAP
# PANEL DE CONTROL DE TAREAS PERSONALES
# METODOS NUMÉRICOS
# Desarrollado por: Indira Moreno y Rene Vega
# Profesor: Ángel Avila
# Proyecto Final
#2025 - I SEMESTRE
#**********************************************

# --- CLASE MAX-HEAP (COLA DE PRIORIDAD) ---

class MaxHeap:
    """
    Implementa un Max-Heap para una Cola de Prioridad.
    La prioridad se basa en el valor más alto del campo 'prioridad' del objeto Tarea.
    """
    def __init__(self):
        # El índice 0 se deja vacío; el Heap comienza en el índice 1 para facilitar el cálculo de padre/hijo.
        self.heap = [None]
        self.task_map = {}  # Mapa auxiliar: {task_id: index_in_heap} para búsquedas rápidas (O(1))

    def _get_parent_index(self, index):
        """Calcula el índice del padre."""
        return index // 2

    def _get_left_child_index(self, index):
        """Calcula el índice del hijo izquierdo."""
        return index * 2

    def _get_right_child_index(self, index):
        """Calcula el índice del hijo derecho."""
        return index * 2 + 1

    def _swap(self, i, j):
        """Intercambia dos elementos en el Heap y actualiza el mapa de tareas."""
        task_i = self.heap[i]
        task_j = self.heap[j]

        # Intercambiar elementos
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        # Actualizar el mapa
        self.task_map[task_i['id']] = j
        self.task_map[task_j['id']] = i

    def _heapify_up(self, index):
        """Ajusta la propiedad del Heap hacia arriba (para inserción o aumento de prioridad)."""
        while index > 1 and self.heap[self._get_parent_index(index)]['prioridad'] < self.heap[index]['prioridad']:
            parent_index = self._get_parent_index(index)
            self._swap(index, parent_index)
            index = parent_index

    def _heapify_down(self, index):
        """Ajusta la propiedad del Heap hacia abajo (para extracción o disminución de prioridad)."""
        n = len(self.heap) - 1
        while True:
            left_child_index = self._get_left_child_index(index)
            right_child_index = self._get_right_child_index(index)
            largest = index

            # Buscar el hijo con mayor prioridad
            if left_child_index <= n and self.heap[left_child_index]['prioridad'] > self.heap[largest]['prioridad']:
                largest = left_child_index

            if right_child_index <= n and self.heap[right_child_index]['prioridad'] > self.heap[largest]['prioridad']:
                largest = right_child_index

            # Si el padre no es el mayor, intercambiar y continuar
            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break

    def insert(self, task):
        """Agrega una nueva tarea al Heap (O(log n))."""
        self.heap.append(task)
        new_index = len(self.heap) - 1
        self.task_map[task['id']] = new_index
        self._heapify_up(new_index)

    def extract_max(self):
        """Extrae la tarea con la máxima prioridad (la Raíz) (O(log n))."""
        if len(self.heap) <= 1:
            return None

        # Tarea máxima es la raíz
        max_task = self.heap[1]

        # Mover la última hoja a la raíz y eliminar el último elemento
        last_index = len(self.heap) - 1
        if last_index > 1:
            self.heap[1] = self.heap.pop()
            self.task_map[self.heap[1]['id']] = 1
            self.task_map.pop(max_task['id'], None)
            self._heapify_down(1)
        else:
            # Solo quedaba la raíz (índice 1)
            self.heap.pop()
            self.task_map.pop(max_task['id'], None)

        return max_task

    def is_empty(self):
        """Verifica si el Heap está vacío."""
        return len(self.heap) <= 1

    def peek_max(self):
        """Retorna la tarea de máxima prioridad sin eliminarla."""
        return self.heap[1] if len(self.heap) > 1 else None

    def change_priority(self, task_id, new_priority):
        """
        Cambia la prioridad de una tarea existente.
        Requiere el mapa auxiliar para ser O(log n) total.
        """
        index = self.task_map.get(task_id)
        if index is None:
            return False

        old_priority = self.heap[index]['prioridad']
        self.heap[index]['prioridad'] = new_priority

        if new_priority > old_priority:
            self._heapify_up(index)  # La prioridad aumentó, se mueve hacia la raíz
        elif new_priority < old_priority:
            self._heapify_down(index) # La prioridad disminuyó, se mueve hacia las hojas

        return True

    def get_all_tasks(self):
        """Retorna una copia de la lista de tareas (sin el None inicial)."""
        # Se retorna una copia, no el heap interno, ya que el orden interno no está totalmente ordenado.
        return self.heap[1:]

    def get_task_by_id(self, task_id):
        """Obtiene la tarea por ID para mostrar detalles."""
        index = self.task_map.get(task_id)
        return self.heap[index] if index else None

# --- FUNCIONES DE UTILIDAD DE LA APLICACIÓN ---

def clear_screen():
    """Limpia la consola. Usa 'cls' para Windows y 'clear' para Unix/Linux/Mac."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Muestra la pantalla de inicio con los datos solicitados."""
    clear_screen()
    print("=" * 70)


    print(" " * 15 + "U N I V E R S I D A D    D E   P A N A M Á")
    print(" " * 10 + "FACULTAD DE INFORMÁTICA, ELECTRÓNICA Y COMUNICACIÓN")
    print(" " * 17 + "PANEL DE CONTROL DE TAREAS PERSONALES")
    print(" " * 15 + "Desarrollado por: Indira Moreno 3-726-1830 ")
    print(" " * 34 + "Rene Vega - 8-882-289" )
    print(" " * 25 + "Profesor: Ángel Avila")
    print(" " * 25 + "ESTRUCTURA DE DATOS")
    print("=" * 70)

def display_menu():
    """Muestra las opciones del menú."""
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar nueva tarea")
    print("2. Ver tarea más urgente (Raíz del Heap)")
    print("3. Marcar la tarea urgente como COMPLETADA")
    print("4. Ver lista completa de tareas")
    print("5. Cambiar prioridad de una tarea")
    print("6. Salir")
    print("-" * 20)

def add_new_task(heap):
    """Lógica para agregar una tarea al Heap."""
    print("\n--- AGREGAR NUEVA TAREA ---")
    description = input("Descripción de la tarea: ")

    while True:
        try:
            # Asegura que la prioridad esté en el rango de 1 a 5
            priority = int(input("Nivel de prioridad (1-5, donde 5 es Máxima Urgencia): "))
            if 1 <= priority <= 5:
                break
            else:
                print("Error: La prioridad debe ser un número entre 1 y 5.")
        except ValueError:
            print("Error: Ingrese un número entero válido para la prioridad.")


    task_id = str(uuid.uuid4().int)[:8]

    new_task = {
        'id': task_id,
        'descripcion': description,
        'prioridad': priority,
        'timestamp': time.time()
    }

    heap.insert(new_task)
    print(f"\n¡Tarea '{description}' agregada con éxito! ID: {task_id}")
    input("\nPresione Enter para continuar...")

def view_max_task(heap):
    """Lógica para ver la tarea con la máxima prioridad."""
    print("\n--- TAREA MÁS URGENTE ---")
    task = heap.peek_max()
    if task:
        print(f"ID: {task['id']}")
        print(f"Descripción: {task['descripcion']}")
        print(f"PRIORIDAD: {task['prioridad']} (¡MÁXIMA URGENCIAS!)")
    else:
        print("¡La lista de tareas está vacía! ¡Felicidades!")
    input("\nPresione Enter para continuar...")

def complete_max_task(heap):
    """Lógica para eliminar la tarea con la máxima prioridad."""
    print("\n--- COMPLETAR TAREA URGENTE ---")
    task = heap.extract_max()
    if task:
        print(f"¡Tarea '{task['descripcion']}' completada y eliminada!")
        new_max = heap.peek_max()
        if new_max:
             print(f"\nLa nueva tarea más urgente ahora es: '{new_max['descripcion']}' (Prioridad: {new_max['prioridad']}).")
        else:
             print("La lista de tareas ha quedado vacía.")
    else:
        print("No hay tareas pendientes para completar.")
    input("\nPresione Enter para continuar...")

def list_all_tasks(heap):
    """Lógica para mostrar todas las tareas en la lista."""
    print("\n--- LISTA COMPLETA DE TAREAS PENDIENTES ---")
    tasks = heap.get_all_tasks()

    if not tasks:
        print("La lista de tareas está vacía.")
        input("\nPresione Enter para continuar...")
        return

    # Se ordena la lista completa en memoria para mejor visualización,
    # aunque el Heap solo garantiza que la Raíz sea el máximo.
    sorted_tasks = sorted(tasks, key=lambda x: x['prioridad'], reverse=True)

    print(f"{'ID':<10} {'Prioridad':<10} {'Descripción'}")
    print("-" * 60)
    for task in sorted_tasks:
        print(f"{task['id']:<10} {task['prioridad']:<10} {task['descripcion']}")

    input("\nPresione Enter para continuar...")

def update_priority(heap):
    """Lógica para cambiar la prioridad de una tarea."""
    print("\n--- CAMBIAR PRIORIDAD ---")

    # Mostrar las tareas actuales para que el usuario elija
    tasks = heap.get_all_tasks()
    if not tasks:
        print("No hay tareas para modificar.")
        input("\nPresione Enter para continuar...")
        return

    list_all_tasks(heap)

    task_id = input("\nIngrese el ID de la tarea a modificar: ")
    task = heap.get_task_by_id(task_id)

    if not task:
        print(f"Error: No se encontró la tarea con ID: {task_id}")
        input("\nPresione Enter para continuar...")
        return

    print(f"Tarea seleccionada: '{task['descripcion']}' (Prioridad actual: {task['prioridad']})")

    while True:
        try:
            new_priority = int(input("Ingrese la NUEVA prioridad (1-5): "))
            if 1 <= new_priority <= 5:
                break
            else:
                print("Error: La prioridad debe ser un número entre 1 y 5.")
        except ValueError:
            print("Error: Ingrese un número entero válido para la nueva prioridad.")

    if heap.change_priority(task_id, new_priority):
        print(f"\nPrioridad de la tarea {task_id} actualizada a {new_priority}.")
        print("El Heap se ha reajustado automáticamente.")
    else:
        print("Error al intentar cambiar la prioridad. Tarea no encontrada.")

    input("\nPresione Enter para continuar...")


# --- LÓGICA PRINCIPAL DE AUTENTICACIÓN Y MENÚ ---

# --- LÓGICA PRINCIPAL DE AUTENTICACIÓN Y MENÚ ---

def main():
    """Función principal de la aplicación."""

    # 1. PANTALLA DE INICIO Y AUTENTICACIÓN FICTICIA
    show_header()

    # Credenciales Ficticias
    correct_user = "admin"
    correct_pass = "admin"

    logged_in = False
    max_attempts = 3
    attempts = 0

    while not logged_in and attempts < max_attempts:
        print("\n--- INICIO DE SESIÓN ---")
        # --- CAMBIO APLICADO AQUÍ ---
        # Se agrega el valor de prueba "Admin" al prompt para guiar al usuario.
        user = input("Usuario:(Admin) ")
        password = input("Clave:(Admin) ")
        # ------------------------------

        if user == correct_user and password == correct_pass:
            logged_in = True
            print("\n¡Inicio de sesión exitoso! Accediendo al panel...")
            time.sleep(1)
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"\nError: Credenciales incorrectas. Intentos restantes: {remaining}")
            if remaining > 0:
                input("Presione Enter para intentar de nuevo...")
                show_header()
            else:
                print("Demasiados intentos fallidos. Saliendo del programa.")
                return

    if not logged_in:
        return

    # ... (El resto de la función main() continúa igual)
    # 2. INICIALIZACIÓN DE LA APLICACIÓN
    task_heap = MaxHeap()
    
    # Datos de ejemplo para empezar
    task_heap.insert({'id': '77800101', 'descripcion': 'Revisar informe final de tesis', 'prioridad': 5, 'timestamp': time.time()})
    task_heap.insert({'id': '77800102', 'descripcion': 'Responder emails pendientes', 'prioridad': 3, 'timestamp': time.time()})
    task_heap.insert({'id': '77800103', 'descripcion': 'Comprar víveres para la semana', 'prioridad': 1, 'timestamp': time.time()})

    # 3. BUCLE PRINCIPAL DEL MENÚ
    while True:
        clear_screen()
        show_header()
        
        # Muestra la tarea actual de máxima prioridad en la parte superior del menú
        max_task = task_heap.peek_max()
        print("\n" + "=" * 70)
        if max_task:
            print(f"| TAREA URGENTE ACTUAL (RAÍZ): {max_task['descripcion']} (P: {max_task['prioridad']})")
        else:
            print("| LISTA VACÍA: ¡Tiempo de descansar!")
        print("=" * 70)
        
        display_menu()

        choice = input("Seleccione una opción: ")

        if choice == '1':
            add_new_task(task_heap)
        elif choice == '2':
            view_max_task(task_heap)
        elif choice == '3':
            complete_max_task(task_heap)
        elif choice == '4':
            list_all_tasks(task_heap)
        elif choice == '5':
            update_priority(task_heap)
        elif choice == '6':
            clear_screen()
            print("Saliendo del Panel de Control. ¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")
            input("Presione Enter para continuar...")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()