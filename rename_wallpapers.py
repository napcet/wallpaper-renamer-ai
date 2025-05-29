import os
import re
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import uuid
import shutil  # necessário para copiar ou mover arquivos
from datetime import datetime


# Inicializa o modelo e processador BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# Pasta onde estão os wallpapers
WALLPAPER_DIR = "wallpapers"
DESTINO_RENOMEADOS = "renomeados"

def gerar_sufixo_contador(contador):
    """
    Gera um sufixo com base na data atual (DDMMAA) e um contador incremental.
    Ex: 290524_1
    """
    prefixo = datetime.now().strftime("%d%m%y")  # Ex: 290524
    return f"{prefixo}_{contador}"


def gerar_nome_descritivo(imagem_path):
    """
    Gera uma descrição textual do conteúdo da imagem usando o modelo BLIP.

    Args:
        imagem_path (str): Caminho para o arquivo da imagem.

    Returns:
        str: Uma legenda descritiva gerada pela IA.
    """
    image = Image.open(imagem_path).convert('RGB')
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# def limpar_nome(nome):
#     nome = nome.lower()
#     nome = re.sub(r'\s+', '-', nome)
#     nome = re.sub(r'[^a-z0-9\-]', '', nome)
#     return nome[:50]

def limpar_nome(nome):
    """
    Processa a descrição para criar um nome de arquivo curto, removendo palavras comuns
    e duplicadas, e limitando a no máximo 4 palavras.

    Args:
        nome (str): Texto descritivo da imagem.

    Returns:
        str: Nome limpo e amigável para uso como nome de arquivo.
    """
    stopwords = {"a", "the", "of", "in", "on", "with", "and", "to", "at", "by", "for", "an", "into", "over", "under", "from"}
    nome = nome.lower()
    palavras = re.findall(r'\b\w+\b', nome)
    palavras = [p for p in palavras if p not in stopwords]

    # Remover palavras duplicadas preservando a ordem
    seen = set()
    palavras_unicas = []
    for p in palavras:
        if p not in seen:
            palavras_unicas.append(p)
            seen.add(p)

    # Limitar a 3-4 palavras principais
    palavras_final = palavras_unicas[:4]

    nome_final = "-".join(palavras_final)
    return nome_final[:40]  # ainda limitamos para evitar nomes longos demais


# def renomear_wallpapers():
#     for nome_arquivo in os.listdir(WALLPAPER_DIR):
#         caminho_completo = os.path.join(WALLPAPER_DIR, nome_arquivo)

#         if not os.path.isfile(caminho_completo):
#             continue

#         try:
#             descricao = gerar_nome_descritivo(caminho_completo)
#             nome_limpo = limpar_nome(descricao)
#             extensao = os.path.splitext(nome_arquivo)[1]
#             novo_nome = f"{nome_limpo}-{uuid.uuid4().hex[:6]}{extensao}"
#             novo_caminho = os.path.join(WALLPAPER_DIR, novo_nome)
#             os.rename(caminho_completo, novo_caminho)
#             print(f"Renomeado: {nome_arquivo} → {novo_nome}")
#         except Exception as e:
#             print(f"Erro com {nome_arquivo}: {e}")

def renomear_wallpapers():
    """
    Processa todas as imagens na pasta 'wallpapers/', gera nomes descritivos,
    e copia os arquivos renomeados para a pasta 'renomeados/'.
    """
    contador = 1
    os.makedirs(DESTINO_RENOMEADOS, exist_ok=True)

    for nome_arquivo in os.listdir(WALLPAPER_DIR):
        caminho_completo = os.path.join(WALLPAPER_DIR, nome_arquivo)

        if not os.path.isfile(caminho_completo):
            continue

        try:
            descricao = gerar_nome_descritivo(caminho_completo)
            nome_limpo = limpar_nome(descricao)
            extensao = os.path.splitext(nome_arquivo)[1]
            sufixo = gerar_sufixo_contador(contador)
            novo_nome = f"{nome_limpo}-{sufixo}{extensao}"
            contador += 1

            novo_caminho = os.path.join(DESTINO_RENOMEADOS, novo_nome)

            shutil.copy2(caminho_completo, novo_caminho)  # ou shutil.move para mover em vez de copiar
            print(f"Renomeado: {nome_arquivo} → {novo_nome}")
        except Exception as e:
            print(f"Erro com {nome_arquivo}: {e}")


if __name__ == "__main__":
    renomear_wallpapers()
