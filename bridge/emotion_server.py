import socket
import json
import rospy
from std_msgs.msg import String

# Funzione che gestisce la connessione del server e la pubblicazione delle emozioni
def emotion_server_program():
    host = socket.gethostname()
    port = 8000  # Porta separata per il server delle emozioni

    # Crea un socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))

    rospy.init_node('emotion_server_node', anonymous=True)  # Inizializza il nodo ROS

    # Crea un publisher per il topic /social/emotion
    emotion_publisher = rospy.Publisher('/social/emotion', String, queue_size=10)

    while True:
        # Aspetta una connessione del client
        server_socket.listen(1)
        conn, address = server_socket.accept()

        while True:
            data = conn.recv(1024).decode()  # Riceve i dati dal client
            if not data:
                break

            try:
                # Decodifica la stringa JSON ricevuta in un dizionario
                parsed_data = json.loads(data)

                # Estrai il valore 'emotion'
                emotion = parsed_data.get('emotion')
                if emotion:
                    # Pubblica l'emozione nel topic /social/emotion
                    emotion_publisher.publish(emotion)
		    print('emotion', emotion)
                else:
                    print("Invalid input")

            except json.JSONDecodeError:
                print("Invalid input")  # Stampa in caso di errore nel parsing

        conn.close()

if __name__ == '__main__':
    emotion_server_program()

