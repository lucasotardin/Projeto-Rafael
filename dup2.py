from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

def replicate_image(image_path, n, output_path):
    img = Image.open(image_path)
    width, height = img.size
    
    # Aumenta as dimensões da imagem
    new_width = width * n
    new_height = height * n
    
    # Cria uma nova imagem vazia
    with Image.new("RGB", (new_width, new_height)) as new_img:
        for i in range(n):
            for j in range(n):
                new_img.paste(img, (i * width, j * height))
        
        # Salva a imagem após todos os blocos serem adicionados
        new_img.save(output_path, format="TIFF", compression="tiff_lzw")

# Solicita ao usuário o valor de n
while True:
    try:
        n = int(input("Digite o valor de n para replicação da imagem: "))
        break
    except ValueError:
        print("Por favor, insira um número inteiro válido.")

# Caminho da imagem
image_path = input("Digite o caminho da imagem JPG: ")

# Caminho de saída para a nova imagem
output_path = input("Digite o caminho de saída para a nova imagem TIFF: ")

# Chama a função para replicar a imagem
try:
    replicate_image(image_path, n, output_path)
    print("Imagem replicada com sucesso!")
except MemoryError:
    print("Erro de memória. Reduza o valor de n ou tente em um sistema com mais memória.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
