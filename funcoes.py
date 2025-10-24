import cv2
import numpy as np

EMOJI_SIZE = 100

# Carrega e redimensiona imagem com transparência
def load_and_resize(path, size=EMOJI_SIZE):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    # Garante 4 canais (BGRA)
    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge((b, g, r, alpha))
    return img

# Função para sobrepor imagem com transparência
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]

    # Ajusta tamanho se estiver fora da tela
    if y + h > background.shape[0]:
        h = background.shape[0] - y
        overlay = overlay[:h, :, :]
    if x + w > background.shape[1]:
        w = background.shape[1] - x
        overlay = overlay[:, :w, :]

    # Garante que background tenha 3 canais
    if background.shape[2] == 4:
        background = cv2.cvtColor(background, cv2.COLOR_BGRA2BGR)

    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha[:h, :w] * overlay[:h, :w, c] +
            (1 - alpha[:h, :w]) * background[y:y+h, x:x+w, c]
        )

    return background

# Função para carregar os emojis (feliz, neutro, triste)
def carregar_emojis():
    face_happy = load_and_resize("face_happy.png")
    face_neutral = load_and_resize("face_neutral.png")
    face_sad = load_and_resize("face_sad.png")
    face_cinema = load_and_resize("face_cinema.png")  # Novo emoji
    return face_happy, face_neutral, face_sad, face_cinema

def mao_aberta(hand_landmarks):
    """
    Retorna True se a mão estiver aberta.
    Considera aberta se pelo menos 3 dedos estiverem estendidos.
    """
    dedos_abertos = 0
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        # Se a ponta está acima da articulação, o dedo está estendido
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            dedos_abertos += 1

    # Retorna True se pelo menos 3 dedos estiverem estendidos
    return dedos_abertos >= 3

