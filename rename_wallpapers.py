import os
import re
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from datetime import datetime

# Inicializa o modelo e processador BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

EXTENSOES_VALIDAS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
WALLPAPER_DIR = "wallpapers"
DESTINO_RENOMEADOS = "renomeados"


def gerar_sufixo_contador(contador):
    """
    Retorna um sufixo com data atual e número sequencial formatado (ex: 290524_001)
    """
    data = datetime.now().strftime("%d%m%y")
    return f"{data}_{contador:03d}"


def gerar_nome_descritivo(imagem_path):
    """
    Gera uma descrição textual da imagem usando BLIP.
    """
    image = Image.open(imagem_path).convert('RGB')
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def limpar_nome(nome):
    """
    Gera um nome com no mínimo 4 palavras e exatamente 25 caracteres.
    Preenche com palavras genéricas se necessário e trunca corretamente.
    """
    stopwords = {"a", "the", "of", "in", "on", "with", "and", "to", "at", "by", "for", "an", "into", "over", "under", "from"}
    palavras_reserva = ["wallpaper", "background", "scene", "image", "landscape", "view"]

    nome = nome.lower()
    palavras = re.findall(r'\b\w+\b', nome)
    palavras = [p for p in palavras if p not in stopwords]

    seen = set()
    palavras_unicas = []
    for p in palavras:
        if p not in seen:
            palavras_unicas.append(p)
            seen.add(p)

    while len(palavras_unicas) < 4:
        for extra in palavras_reserva:
            if extra not in palavras_unicas:
                palavras_unicas.append(extra)
                if len(palavras_unicas) == 4:
                    break

    for i in range(4, 0, -1):
        tentativa = "-".join(palavras_unicas[:i])
        if len(tentativa) <= 25:
            return tentativa.ljust(25, "-")

    return "-".join(palavras_unicas)[:25]


def renomear_wallpapers():
    """
    Processa imagens, gera nomes descritivos de 25 caracteres, converte para JPEG e salva com sufixo padronizado.
    """
    contador = 1
    os.makedirs(DESTINO_RENOMEADOS, exist_ok=True)

    for nome_arquivo in os.listdir(WALLPAPER_DIR):
        caminho_completo = os.path.join(WALLPAPER_DIR, nome_arquivo)

        if (
            not os.path.isfile(caminho_completo)
            or os.path.splitext(nome_arquivo)[1].lower() not in EXTENSOES_VALIDAS
        ):
            continue

        try:
            descricao = gerar_nome_descritivo(caminho_completo)
            nome_limpo = limpar_nome(descricao)
            sufixo = gerar_sufixo_contador(contador)
            contador += 1

            novo_nome = f"{nome_limpo}-{sufixo}.jpg"
            novo_caminho = os.path.join(DESTINO_RENOMEADOS, novo_nome)

            imagem = Image.open(caminho_completo).convert("RGB")
            imagem.save(novo_caminho, format="JPEG", quality=90)

            print(f"Convertido e renomeado: {nome_arquivo} → {novo_nome}")
        except Exception as e:
            print(f"Erro com {nome_arquivo}: {e}")


if __name__ == "__main__":
    renomear_wallpapers()