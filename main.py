import cv2
import mediapipe as mp
import numpy as np

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)
mp_drawings = mp.solutions.drawing_utils

# Tamanho do emoji
EMOJI_SIZE = 100

# Carrega imagens e redimensiona
def load_and_resize(path, size=EMOJI_SIZE):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    # Garante 4 canais
    if img.shape[2] == 3:
        b, g, r = cv2.split(img)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge((b, g, r, alpha))
    return img

face_happy = load_and_resize("face_happy.png")
face_neutral = load_and_resize("face_neutral.png")
face_sad = load_and_resize("face_sad.png")

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

    # Garantir que background tenha 3 canais
    if background.shape[2] == 4:
        background = cv2.cvtColor(background, cv2.COLOR_BGRA2BGR)

    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha[:h, :w] * overlay[:h, :w, c] +
            (1 - alpha[:h, :w]) * background[y:y+h, x:x+w, c]
        )

    return background

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    expression = "neutral"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Pega pontos da boca e olhos
            mouth_top = face_landmarks.landmark[13]
            mouth_bottom = face_landmarks.landmark[14]
            left_eye = face_landmarks.landmark[159]
            right_eye = face_landmarks.landmark[386]

            # Calcula abertura da boca e olhos
            mouth_open = abs(mouth_bottom.y - mouth_top.y)
            eye_open = abs(left_eye.y - right_eye.y)

            # Define expressão simples
            if mouth_open > 0.04:
                expression = "feliz"
            elif mouth_open < 0.02:
                expression = "triste"
            else:
                expression = "neutro"

    # Posição do emoji
    emoji_x = frame.shape[1] - EMOJI_SIZE - 20
    emoji_y = frame.shape[0] - EMOJI_SIZE - 20

    # Aplica emoji conforme expressão
    if expression == "feliz":
        frame = overlay_image(frame, face_happy, emoji_x, emoji_y)
    elif expression == "triste":
        frame = overlay_image(frame, face_sad, emoji_x, emoji_y)
    else:
        frame = overlay_image(frame, face_neutral, emoji_x, emoji_y)

    cv2.putText(frame, f"Expressao: {expression}", (30, frame.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Reconhecimento de Expressao Facial", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC -> sair
        break

cap.release()
cv2.destroyAllWindows()
