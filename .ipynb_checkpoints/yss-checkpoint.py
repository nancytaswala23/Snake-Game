
import socket
from ast import literal_eval
import random

HOST = '0.0.0.0'
PORT = 5001  # Port for the yellow snake

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_sock, client_addr = s.accept()
        print('New connection from', client_addr)

        while True:
            data = client_sock.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                x1, y1, x2, y2, rx1, ry1, rx2, ry2, ax, ay = literal_eval(data.decode())

                print(x1, y1, x2, y2, "red:", rx1, ry1, rx2, ry2, "apple:", ax, ay)

                # Chase apple while ensuring no out-of-bounds movement
                move_options = []

                if x1 < ax and x1 + SEG_SIZE < WIDTH:  # Move right if safe
                    move_options.append("Right")
                elif x1 > ax and x1 - SEG_SIZE >= 0:  # Move left if safe
                    move_options.append("Left")

                if y1 < ay and y1 + SEG_SIZE < HEIGHT:  # Move down if safe
                    move_options.append("Down")
                elif y1 > ay and y1 - SEG_SIZE >= 0:  # Move up if safe
                    move_options.append("Up")

                if move_options:
                    data_to_proxy = random.choice(move_options)
                else:
                    # Random safe movement if no valid move towards apple
                    safe_moves = []
                    if x1 + SEG_SIZE < WIDTH:
                        safe_moves.append("Right")
                    if x1 - SEG_SIZE >= 0:
                        safe_moves.append("Left")
                    if y1 + SEG_SIZE < HEIGHT:
                        safe_moves.append("Down")
                    if y1 - SEG_SIZE >= 0:
                        safe_moves.append("Up")

                    data_to_proxy = random.choice(safe_moves) if safe_moves else "Straight"

                print(f"Sending direction: {data_to_proxy}")
                client_sock.sendall(data_to_proxy.encode())

            else:
                break

        client_sock.close()
    s.close()

