#client_test

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 5000))

    while True:
        testo = input("Messaggio (scrivi esci per terminare): ")

        if testo.lower() == "esci":
            break

        client.sendall(testo.encode("utf-8"))

        risposta = client.recv(1024)
        print(risposta.decode("utf-8"))
