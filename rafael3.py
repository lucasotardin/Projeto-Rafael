import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import cv2
import numpy as np
import time

# Função para carregar a imagem grande usando PIL e convertê-la para o formato do OpenCV
def carregar_imagem_grande(imagem_path):
    imagem = Image.open(imagem_path)
    imagem = np.array(imagem)
    return imagem

# Carregando a imagem
imagem_path = 'car250.tiff'
start_time = time.time()
if os.path.exists(imagem_path):
    imagem = carregar_imagem_grande(imagem_path)
else:
    print(f"Erro: a imagem '{imagem_path}' não foi encontrada.")
    exit()

# Converter para escala de cinza

cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Invertendo as cores
inverted = cv2.bitwise_not(cinza)

# Limiarização da imagem para destacar os carros
_, binaria = cv2.threshold(inverted, 127, 255, cv2.THRESH_BINARY)

# Encontrar contornos na imagem
  # Início do temporizador antes de encontrar os contornos
contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
end_time = time.time()  # Fim do temporizador após encontrar os contornos

# Variável para contar carros identificados
num_carros = 0

# Desenhar contornos ao redor dos carros
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 1000:  # Ajuste este valor conforme necessário
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)
        num_carros += 1

# Calcular o tempo de execução
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"Tempo de execução: {minutes} minutos {seconds:.2f} segundos")
print("Número de carros identificados:", num_carros)

# Salvar a imagem com os carros identificados
cv2.imwrite('carros_identificados.tiff', imagem)

# Exibindo a imagem com os contornos dos carros identificados
cv2.imshow('Carros Identificados', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
