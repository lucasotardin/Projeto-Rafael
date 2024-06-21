import os
from PIL import Image
import cv2
import numpy as np
import time

Image.MAX_IMAGE_PIXELS = None

# Função para carregar pedaços da imagem grande usando PIL e convertê-la para o formato do OpenCV
def carregar_pedacos_imagem_grande(imagem_path, bloco_tamanho=1024):
    imagem = Image.open(imagem_path)
    largura, altura = imagem.size
    return largura, altura, imagem

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

# Caminho da imagem
imagem_path = 'car300.tiff'
bloco_tamanho = 1024

start_time = time.time()
if os.path.exists(imagem_path):
    largura, altura, imagem = carregar_pedacos_imagem_grande(imagem_path, bloco_tamanho)
else:
    print(f"Erro: a imagem '{imagem_path}' não foi encontrada.")
    exit()

# Criar uma imagem vazia para o resultado final
resultado = np.zeros((altura, largura, 3), dtype=np.uint8)

# Processar cada pedaço da imagem
num_carros_total = 0
for y in range(0, altura, bloco_tamanho):
    for x in range(0, largura, bloco_tamanho):
        caixa = (x, y, min(x + bloco_tamanho, largura), min(y + bloco_tamanho, altura))
        pedaco = imagem.crop(caixa)
        pedaco_cv = cv2.cvtColor(np.array(pedaco), cv2.COLOR_RGB2BGR)
        num_carros_total += processar_pedaco(pedaco_cv, x, y, resultado)
        pedaco.close()
        del pedaco_cv  # Explicitamente deletar a variável para liberar memória

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
