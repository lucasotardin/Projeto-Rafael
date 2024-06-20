import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import cv2
import numpy as np
import time

# Função para carregar pedaços da imagem grande usando PIL e convertê-la para o formato do OpenCV
def carregar_pedacos_imagem_grande(imagem_path, bloco_tamanho=1024):
    imagem = Image.open(imagem_path)
    largura, altura = imagem.size
    pedacos = []
    
    for y in range(0, altura, bloco_tamanho):
        for x in range(0, largura, bloco_tamanho):
            caixa = (x, y, x + bloco_tamanho, y + bloco_tamanho)
            pedaco = imagem.crop(caixa)
            pedacos.append((np.array(pedaco), (x, y)))
    
    return pedacos, largura, altura

# Função para processar cada pedaço
def processar_pedaco(pedaco, x_offset, y_offset, resultado):
    # Converter para escala de cinza
    cinza = cv2.cvtColor(pedaco, cv2.COLOR_BGR2GRAY)
    # Invertendo as cores
    inverted = cv2.bitwise_not(cinza)
    # Limiarização da imagem para destacar os carros
    _, binaria = cv2.threshold(inverted, 127, 255, cv2.THRESH_BINARY)
    # Encontrar contornos na imagem
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variável para contar carros identificados
    num_carros = 0

    # Desenhar contornos ao redor dos carros
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 1000:  # Ajuste este valor conforme necessário
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(resultado, (x + x_offset, y + y_offset), (x + x_offset + w, y + y_offset + h), (0, 255, 0), 2)
            num_carros += 1
    
    return num_carros

# Carregando a imagem em pedaços
imagem_path = 'car250.tiff'
start_time = time.time()
if os.path.exists(imagem_path):
    pedacos, largura, altura = carregar_pedacos_imagem_grande(imagem_path)
else:
    print(f"Erro: a imagem '{imagem_path}' não foi encontrada.")
    exit()

# Criar uma imagem vazia para o resultado final
resultado = np.zeros((altura, largura, 3), dtype=np.uint8)

# Processar cada pedaço da imagem
num_carros_total = 0
for pedaco, (x_offset, y_offset) in pedacos:
    num_carros_total += processar_pedaco(pedaco, x_offset, y_offset, resultado)

# Fim do temporizador
end_time = time.time()

# Calcular o tempo de execução
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"Tempo de execução: {minutes} minutos {seconds:.2f} segundos")
print("Número de carros identificados:", num_carros_total)

# Salvar a imagem com os carros identificados
cv2.imwrite('carros_identificados.tiff', resultado)

# Exibindo a imagem com os contornos dos carros identificados
cv2.imshow('Carros Identificados', resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
