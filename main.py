import cv2
import mediapipe as mp
from funcoes import overlay_image, carregar_emojis, mao_aberta, EMOJI_SIZE

mp_face = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face_mesh = mp_face.FaceMesh(refine_landmarks=True)
hands_detector = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5)

# Carrega emojis
face_happy, face_neutral, face_sad, face_cinema = carregar_emojis()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    results_hands = hands_detector.process(rgb)

    expression = "neutro"
    both_hands_open = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mouth_top = face_landmarks.landmark[13]
            mouth_bottom = face_landmarks.landmark[14]
            left_eye = face_landmarks.landmark[159]
            right_eye = face_landmarks.landmark[386]

            mouth_open = abs(mouth_bottom.y - mouth_top.y)
            eye_open = abs(left_eye.y - right_eye.y)

            if mouth_open > 0.04:
                expression = "feliz"
            elif mouth_open < 0.02:
                expression = "triste"
            else:
                expression = "neutro"

    if results_hands.multi_hand_landmarks:
        mp_draw = mp.solutions.drawing_utils
        hands_open = 0

        for idx, hand in enumerate(results_hands.multi_hand_landmarks):
        # Desenha a mão na tela
            mp_draw.draw_landmarks(
               frame,
               hand,
               mp_hands.HAND_CONNECTIONS,
               mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2),
               mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2),
        )

        # Verifica se a mão está aberta
            aberta = mao_aberta(hand)
            if aberta:
                hands_open += 1

        # Mensagem de debug sobre a mão
            texto = f"Mao {idx+1}: {'Aberta' if aberta else 'Fechada'}"
            cv2.putText(frame, texto, (30, 30 + idx*30),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Define a expressão “cinema” se pelo menos 2 mãos abertas
        if hands_open >= 2:
            both_hands_open = True

    if both_hands_open:
        print("Mãos abertas detectadas! ABSOULUTE CINEMA!")
        expression = "cinema"

    emoji_x = frame.shape[1] - EMOJI_SIZE - 20
    emoji_y = frame.shape[0] - EMOJI_SIZE - 20

    if expression == "feliz":
        frame = overlay_image(frame, face_happy, emoji_x, emoji_y)
    elif expression == "triste":
        frame = overlay_image(frame, face_sad, emoji_x, emoji_y)
    elif expression == "cinema":
        frame = overlay_image(frame, face_cinema, emoji_x, emoji_y)
    else:
        frame = overlay_image(frame, face_neutral, emoji_x, emoji_y)

    cv2.putText(frame, f"Expressao: {expression}", (30, frame.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Reconhecimento de Expressao Facial e de Maos", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC -> sair
        break


cap.release()
cv2.destroyAllWindows()
