import os
from abc import ABC, abstractmethod

import cv2
import numpy as np


class NoSourceProvidedError(Exception):
	pass


class FaceLoader:
	def __init__(self, saves_path: str = 'faces', cascade_path: str = "haarcascade_frontalface_default.xml"):
		# self.cascade_path = "haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(cascade_path)
		self.camera_loader = CameraLoader()
		self.file_loader = FileLoader()
		self.trainer = Trainer()
		self._SAVES_PATH = saves_path

	def __str__(self):
		return "Face Loader"

	def load_from_camera(self, face_id, name):
		self.camera_loader.load(self._SAVES_PATH, face_id, name)
		self.trainer.train(self._SAVES_PATH)

	def load_from_file(self, filename, face_id, name):
		self.file_loader.load(self._SAVES_PATH, face_id, name, filename)
		self.trainer.train(self._SAVES_PATH)


class BaseImageLoader(ABC):
	def __init__(self, scale_factor=None, min_neighbors=None, min_size=None):
		self._SCALE_FACTOR = scale_factor or 1.2
		self._MIN_NEIGHBORS = min_neighbors or 5
		self._MIN_SIZE = min_size or (20, 20)
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	@staticmethod
	def _save_face(face_id, num, img, username="user"):
		# TODO: check if folder 'faces' exists
		# TODO: change "user" to username??
		filepath = f"faces/{username}.{face_id}.{num}.jpg"
		cv2.imwrite(filepath, img)

	@abstractmethod
	def load(self, save_path: str, face_id: int, name: str, source=None):
		pass


class CameraLoader(BaseImageLoader):
	def __init__(self, image_count=None, scale_factor=None, min_neighbors=None, min_size=None):
		super().__init__(scale_factor, min_neighbors, min_size)
		self._IMAGE_COUNT = image_count or 30

	def __str__(self):
		return "Camera Loader"

	def load(self, save_path: str, face_id: int = 0, name: str = "user", source=None):
		"""
		Load face image from camera.

		Params:
			face_id: int - unique id of the user
			name: str - name of the user

		Collects 30 different images of user's face by default.
		"""
		count = 0
		cap = cv2.VideoCapture(0)
		cap.set(cv2.CAP_PROP_FPS, 24)
		while True:
			ret, img = cap.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			faces = self.face_cascade.detectMultiScale(
				gray,
				scaleFactor=self._SCALE_FACTOR,
				minNeighbors=self._MIN_NEIGHBORS,
				minSize=self._MIN_SIZE
			)

			for (x, y, w, h) in faces:
				cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
				count += 1
				self._save_face(face_id, count, gray[y:y + h, x:x + w], name)

			cv2.imshow("camera", img)
			k = cv2.waitKey(100) & 0xff  # 'ESC'
			if k == 27 or count >= 30:
				break

		cap.release()
		cv2.destroyAllWindows()


class FileLoader(BaseImageLoader):
	def __init__(self, scale_factor=None, min_neighbors=None, min_size=None):
		super().__init__(scale_factor, min_neighbors, min_size)

	def __str__(self):
		return "File loader"

	def load(self, save_path: str, face_id: int, name: str, source=None):
		if source is None:
			raise NoSourceProvidedError
		img = cv2.imread(source)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		x, y, w, h = self.face_cascade.detectMultiScale(
			gray,
			scaleFactor=self._SCALE_FACTOR,
			minNeighbors=self._MIN_NEIGHBORS,
			minSize=self._MIN_SIZE
		)[0]
		count = len(list(filter(lambda f: int(f.split('.')[1]) == face_id, os.listdir(save_path))))
		self._save_face(face_id, count+1, gray[y:y + h, x:x + w])


class Trainer:
	def __init__(self):
		pass

	def __str__(self):
		return "Trainer"

	@staticmethod
	def _get_faces_and_ids(path: str):
		img_paths = [os.path.join(path, f) for f in os.listdir(path)]
		faces = []
		ids = []

		for img_path in img_paths:
			img = cv2.imread(img_path)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			faces.append(gray)
			face_id = int(os.path.split(img_path)[-1].split('.')[1])
			ids.append(face_id)

		return faces, ids

	def train(self, path: str):
		faces, ids = self._get_faces_and_ids(path)
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.train(faces, np.array(ids))
		recognizer.write('face.yml')
