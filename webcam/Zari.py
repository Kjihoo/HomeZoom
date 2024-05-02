#자리비움인식
import cv2
import time

# 얼굴 인식을 위한 분류기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 웹캠에서 영상 가져오기 인자가 0이면 기본웹캠
cap = cv2.VideoCapture(0)

# 마지막으로 메시지가 표시된 시간
last_message_time = time.time()

# 이전에 얼굴이 감지된 시간
last_detection_time = time.time()

# 메시지 표시 간격 (초)
message_interval = 5

# 3초 동안 얼굴이 감지된 횟수
detection_count = 0

while True:
    # 영상 프레임 읽기
    ret, frame = cap.read()

    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 얼굴이 감지되었는지 확인
    if len(faces) > 0:
        last_detection_time = time.time()
        detection_count += 1

    # 5초가 지났는지 확인하고 메시지 출력
    current_time = time.time()
    if current_time - last_message_time >= message_interval:
        last_message_time = current_time
        if detection_count > 0:
            print("얼굴이 감지되었습니다.")
            print(detection_count)
        else:
            print("얼굴이 감지되지 않았습니다.")
        detection_count = 0

    # 3초 동안 얼굴이 감지되었는지 확인
    if current_time - last_detection_time > message_interval:
        detection_count = 0

    # 영상에 얼굴 표시
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 영상 출력
    cv2.imshow('frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
