# 😃 Reconhecimento de Expressões Faciais com Imagens

Este projeto utiliza **Visão Computacional** com **OpenCV** e **MediaPipe** para detectar expressões faciais em tempo real e exibir emojis correspondentes às emoções identificadas (feliz, triste ou neutro).

---

## 🧩 Funcionalidades

- Captura facial em tempo real usando webcam 🎥  
- Reconhecimento de expressões com MediaPipe Face Mesh  
- Exibição dinâmica de imagens conforme a expressão detectada 😃😐😢  
- Interface simples e intuitiva com OpenCV  

---

## 🖼️ Expressões Detectadas

| Emoção | Descrição | Reação |
|:-------|:-----------|:------|
| **Feliz** | Sorriso detectado | 😃 |
| **Neutra** | Sem variação facial | 😐 |
| **Triste** | Curvatura negativa da boca | 😢 |

---

## 🧰 Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://developers.google.com/mediapipe)
- [NumPy](https://numpy.org/)

---

## 🚀 Como Executar o Projeto

1. **Clone este repositório**
   ```bash
   git clone https://github.com/josephgabriel/ExpressoesFaciais.git
   cd ExpressoesFaciais
2. Crie e ative um ambiente virtual (opcional, mas recomendado)
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Zorin
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute o script principal
```bash
python main.py
```

Permita o acesso à webcam e veja a mágica acontecer! ✨

