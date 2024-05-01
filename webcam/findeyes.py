import cv2
import numpy as np
import pyvirtualcam
import dlib
from imutils import face_utils
from keras.models import load_model
import time

# 이미지 크기 설정
IMG_SIZE = (34, 26)
CAM_WIDTH = 640
CAM_HEIGHT = 480

# dlib을 사용하여 얼굴 및 눈을 검출하기 위한 detector 및 predictor 객체 생성
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 미리 학습된 딥러닝 모델 로드
model = load_model('models/eyes.h5')

# 눈 이미지를 잘라내는 함수 정의
def crop_eye(img, eye_points):
    # 눈의 왼쪽 상단과 오른쪽 하단 좌표를 찾아냄
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    # 눈의 중심점 계산
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    # 눈 영역의 너비와 높이 계산
    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]

    # 눈 영역 주변의 여유 공간(margin) 계산
    margin_x, margin_y = w / 2, h / 2

    # 눈 영역의 좌상단과 우하단 좌표 계산
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    # 눈 영역 추출
    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    return eye_img, eye_rect


#pyvi어쩌구로 가상 카메라 만드는거
with pyvirtualcam.Camera(width=CAM_WIDTH, height=CAM_HEIGHT, fps=30) as cam:

# 웹캠 열기
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # 웹캠에서 프레임 읽기
        ret, img_ori = cap.read()

        if not ret:
            break

        # 이미지 좌우 반전
        img = cv2.flip(img_ori, 1)
        # 그레이스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # dlib을 사용하여 얼굴 검출
        faces = detector(gray)

        # 각 얼굴에 대해 반복
        for face in faces:
            # 얼굴의 특징점 검출
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)

            # 얼굴 영역에서 눈 영역 잘라내기
            eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

            # 눈 이미지 크기 조정
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            # 딥러닝 모델에 눈 이미지 입력 후 예측
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            pred_l = model.predict(eye_input_l) * 100
            pred_r = model.predict(eye_input_r) * 100

            # 눈의 상태에 따라 텍스트 및 사각형 그리기
            state_l = 'O %.1f' if pred_l > 10 else '- %.1f'
            state_r = 'O %.1f' if pred_r > 10 else '- %.1f'
            state_l = state_l % pred_l
            state_r = state_r % pred_r
            cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255), thickness=2)
            cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255), thickness=2)
            cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 결과 이미지 출력
        #cv2.imshow('result', img)

        time.sleep(0.02)

        #OBS에 맞는 RGB 색상공간 변경
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #처리한 캠 obs에 보내기
        cam.send(rgb_img)
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) == ord('q'):
            break

# 웹캠 해제 및 윈도우 종료
cap.release()
cv2.destroyAllWindows()