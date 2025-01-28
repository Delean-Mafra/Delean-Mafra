import cv2
from pyzbar import pyzbar
import numpy as np

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def read_qr_code():
    # Abre a câmera
    cap = cv2.VideoCapture(0)

    while True:
        # Captura frame por frame
        ret, frame = cap.read()

        # Decodifica o QR code
        decoded_objects = pyzbar.decode(frame)

        # Desenha um retângulo ao redor do QR code e imprime os dados
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points
            
            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            # Imprime os dados do QR code
            qr_data = obj.data.decode("utf-8")
            print("QR Code detected: ", qr_data)

            # Encerra o loop após ler o QR code com sucesso
            cap.release()
            cv2.destroyAllWindows()
            return

        # Mostra o frame resultante
        cv2.imshow('QR Code Scanner', frame)

        # Encerra o loop ao pressionar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Quando tudo estiver concluído, libera a captura e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()

# Executa a função de leitura de QR code
read_qr_code() 
