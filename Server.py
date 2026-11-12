#Server.py

import socket
import threading

HOST = "0.0.0.0"
PORTA = 5000

client_connessi = []


def gestisci_client(connessione, indirizzo):
    print(f"Nuovo client connesso: {indirizzo}")

    try:
        while True:
            messaggio = connessione.recv(1024)

            if not messaggio:
                break

            testo = messaggio.decode("utf-8")
            print(f"{indirizzo}: {testo}")

            risposta = f"Server Delta ha ricevuto: {testo}"
            connessione.sendall(risposta.encode("utf-8"))

    except OSError as errore:
        print(f"Errore con {indirizzo}: {errore}")

    finally:
        connessione.close()
        print(f"Client disconnesso: {indirizzo}")


def avvia_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORTA))
    server.listen()

    print(f"Server Delta in ascolto sulla porta {PORTA}")

    try:
        while True:
            connessione, indirizzo = server.accept()

            thread = threading.Thread(
                target=gestisci_client,
                args=(connessione, indirizzo)
            )

            thread.start()

    except KeyboardInterrupt:
        print("Arresto del server...")

    finally:
        server.close()


if __name__ == "__main__":
    avvia_server()
