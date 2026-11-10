import socket
import json

HOST = "localhost"
PUERTO = 5000


def enviar_tarea(tarea):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PUERTO))
        s.sendall((json.dumps(tarea) + "\n").encode())
        respuesta = s.makefile("r").readline()
        return json.loads(respuesta)


if __name__ == "__main__":
    tareas = [
        {"tipo": "suma", "datos": [1, 2, 3, 4]},
        {"tipo": "mayusculas", "datos": "hola servidor"},
        {"tipo": "suma", "datos": [10, 20, 30]},
    ]
    for t in tareas:
        print(f"Envío: {t}")
        print(f"Recibo: {enviar_tarea(t)}\n")