import os

import cv2


class Authenticator:
	def __init__(
			self,
			yml_path: str = 'face.yml',
			cascade_path: str = "haarcascade_frontalface_default.xml",
			faces_path: str = 'faces',
			confidence_threshold: int = 100
	):
		self.YML_PATH = yml_path
		self.CASCADE_PATH = cascade_path
		self.FACES_PATH = faces_path
		self.__CONFIDENCE_THRESHOLD = confidence_threshold
			
	def __str__(self):
		return "Face authenticator"

	def get_ids_and_names(self):
		"""
		return dict {id: username} of loaded faces
		"""
		return {int(file.split('.')[1]): file.split('.')[0] for file in os.listdir(self.FACES_PATH)}

	def authenticate(self):
		recognizer = self.create_recognizer()
		face_cascade = cv2.CascadeClassifier(self.CASCADE_PATH)
		font = cv2.FONT_HERSHEY_SIMPLEX

		names = self.get_ids_and_names()
		print(names)

		cam = cv2.VideoCapture(0)
		cam.set(3, 640)  # set video width
		cam.set(4, 480)  # set video height

		while True:
			ret, img = cam.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			faces = face_cascade.detectMultiScale(
				gray,
				scaleFactor=1.2,
				minNeighbors=5,
				minSize=(10, 10),
			)

			for (x, y, w, h) in faces:

				id_, confidence = recognizer.predict(gray[y:y + h, x:x + w])

				if confidence < self.__CONFIDENCE_THRESHOLD:
					name = names[id_]
					confidence = "Confidence:  {0}".format(round(self.__CONFIDENCE_THRESHOLD - confidence))
					cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
				else:
					name = "unknown"
					confidence = "Confidence:  {0}".format(round(self.__CONFIDENCE_THRESHOLD - confidence))
					cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

				cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
				cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

			cv2.imshow('camera', img)

			k = cv2.waitKey(10) & 0xff  # 'ESC' для Выхода
			if k == 27:
				break

		cam.release()
		cv2.destroyAllWindows()

	def create_recognizer(self):
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.read(self.YML_PATH)
		return recognizer

	def set_faces_dir(self, new_dir):
		if not os.path.isdir(new_dir):
			raise NotADirectoryError(f"{new_dir} is not a directory")

		self.FACES_PATH = new_dir

	@property
	def confidence_threshold(self):
		return self.__CONFIDENCE_THRESHOLD

	def set_confidence_threshold(self, th: int):
		if not isinstance(th, int) and 0 >= th:
			raise ValueError(f"{th} must be a positive integer")

		self.__CONFIDENCE_THRESHOLD = th
