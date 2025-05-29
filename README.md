# Wallpaper Renamer AI

Renomeia automaticamente wallpapers com base no conteúdo visual da imagem usando inteligência artificial (modelo BLIP da Salesforce).  
Ideal para organizar acervos grandes de imagens de forma rápida, inteligente e sem duplicatas.

---

## 🧠 O que o script faz

- Analisa imagens de uma pasta (`wallpapers/`)
- Gera descrições automáticas usando IA (BLIP)
- Cria nomes curtos e legíveis com base na descrição
- Renomeia os arquivos com base na data e numeração sequencial (ex: `sunset-mountain-290524_1.jpg`)
- Salva os arquivos renomeados em uma nova pasta (`renomeados/`)

---

## 🚀 Como usar

### 🔹 Instalação manual (recomendada para iniciantes)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/wallpaper-renamer-ai.git
cd wallpaper-renamer-ai

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # (Linux/macOS)
# venv\Scripts\activate   # (Windows, use no terminal CMD)

# Instale as dependências
pip install -r requirements.txt

# Coloque suas imagens na pasta 'wallpapers/'
# E execute o script
python rename_wallpapers.py
```
