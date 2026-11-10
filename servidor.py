import socket
import threading
import queue
import json

HOST = "0.0.0.0"
PUERTO = 5000
NUM_WORKERS = 3

cola_tareas = queue.Queue()


def procesar(tarea):
    tipo = tarea.get("tipo")
    datos = tarea.get("datos")
    if tipo == "suma":
        return sum(datos)
    if tipo == "mayusculas":
        return datos.upper()
    return "tarea desconocida"


def worker(id_worker):
    while True:
        tarea, cliente = cola_tareas.get()
        try:
            resultado = procesar(tarea)
            respuesta = {"worker": id_worker, "resultado": resultado}
            cliente.sendall((json.dumps(respuesta) + "\n").encode())
        except OSError as e:
            print(f"[Worker {id_worker}] Error: {e}")
        finally:
            cliente.close()
            cola_tareas.task_done()


def manejar_cliente(cliente, direccion):
    try:
        linea = cliente.makefile("r").readline()
        tarea = json.loads(linea)
        print(f"Tarea de {direccion}: {tarea}")
        cola_tareas.put((tarea, cliente))  # la toma un worker libre
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error con {direccion}: {e}")
        cliente.close()


def main():
    for i in range(1, NUM_WORKERS + 1):
        threading.Thread(target=worker, args=(i,), daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        print(f"Servidor escuchando en {HOST}:{PUERTO} con {NUM_WORKERS} workers")
        while True:
            cliente, direccion = servidor.accept()
            threading.Thread(
                target=manejar_cliente, args=(cliente, direccion), daemon=True
            ).start()


if __name__ == "__main__":
    main()