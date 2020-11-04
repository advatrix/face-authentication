import cv2


face_сascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 24)  # Частота кадров

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_сascade.detectMultiScale(
        gray,               #
        scaleFactor=1.2,    #
        minNeighbors=5,     #
        minSize=(20, 20)    #
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("camera", img)

    if cv2.waitKey(10) == 27:  # Esc key
        break
cap.release()
cv2.destroyAllWindows()
