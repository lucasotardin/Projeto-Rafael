import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import cv2
import numpy as np
import timeit

# Função para carregar a imagem grande usando PIL e convertê-la para o formato do OpenCV
def carregar_imagem_grande(imagem_path):
    imagem = Image.open(imagem_path)
    imagem = np.array(imagem)
    return imagem

# Carregando a imagem
imagem_path = 'car150.tiff'
if os.path.exists(imagem_path):
    imagem = carregar_imagem_grande(imagem_path)
    print("Dimensões da imagem carregada:", imagem.shape)
else:
    print(f"Erro: a imagem '{imagem_path}' não foi encontrada.")
    exit()

# Converter para escala de cinza
cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Invertendo as cores
inverted = cv2.bitwise_not(cinza)

# Limiarização da imagem para destacar os carros
_, binaria = cv2.threshold(inverted, 127, 255, cv2.THRESH_BINARY)

# Definindo a função principal que realiza a detecção de carros
def detectar_carros():
    # Encontrar contornos na imagem
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variável para contar carros identificados
    num_carros = 0

    # Desenhar contornos ao redor dos carros
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 1000:  # Ajuste este valor conforme necessário
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)
            num_carros += 1

# Medir o tempo de execução utilizando timeit
tempo_execucao = timeit.timeit(stmt=detectar_carros, number=1)
print("Tempo de execução:", tempo_execucao, "segundos")
