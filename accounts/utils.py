from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile
import random


def generate_default_avatar(name):
    # Define o tamanho da imagem
    size = (100, 100)

    # Cria uma nova imagem com fundo branco
    image = Image.new('RGB', size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Define a cor do círculo
    colors = [(255, 99, 71), (135, 206, 250), (255, 192, 203), (144, 238, 144)]
    background_color = random.choice(colors)

    # Desenha o círculo
    draw.ellipse([0, 0, size[0], size[1]], fill=background_color)

    # Define o tamanho da fonte
    font_size = 50  # Ajuste este valor para o tamanho desejado
    try:
        # Substitua o caminho pela fonte desejada se necessário
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Caso a fonte não seja encontrada, usa a fonte padrão
        font = ImageFont.load_default()

    # Adiciona a inicial do nome
    initial = name[0].upper()

    # Obtém a caixa delimitadora do texto para centralizá-lo
    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calcula as coordenadas para centralizar o texto
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - text_height) / 2 - bbox[1]  # Ajusta a posição vertical

    # Desenha o texto na imagem
    draw.text((text_x, text_y), initial, fill=(255, 255, 255), font=font)

    # Salva a imagem em um arquivo em memória
    image_io = io.BytesIO()
    image.save(image_io, format='PNG')
    image_file = ContentFile(image_io.getvalue(), 'default_avatar.png')

    return image_file
