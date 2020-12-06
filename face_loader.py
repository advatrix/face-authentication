from __future__ import annotations
from typing import Optional

import os
from abc import ABC, abstractmethod

import cv2
import numpy as np


class NoSourceProvidedError(Exception):
	"""
	Exception thrown when there is no source image with faces provided to the Loader.
	"""
	pass


class FaceLoader:
	"""
	Face loading manager.
	"""
	def __init__(self, saves_path: str = 'faces', cascade_path: str = "haarcascade_frontalface_default.xml"):
		self.faceCascade = cv2.CascadeClassifier(cascade_path)
		self.camera_loader = CameraLoader()
		self.file_loader = FileLoader()
		self.trainer = Trainer()
		self._SAVES_PATH = saves_path

	def __str__(self):
		return "Face Loader"

	def load_from_camera(self, face_id: int, name: str):
		"""
		Load face image from camera
		:param face_id: unique id of the user
		:param name: name of the user
		"""
		self.camera_loader.load(self._SAVES_PATH, face_id, name)
		self.trainer.train(self._SAVES_PATH)

	def load_from_file(self, filename: str, face_id: int, name: str):
		"""
		Load face from file
		:param filename: source of the image
		:param face_id: unique id of the user
		:param name: name of the user
		"""
		self.file_loader.load(self._SAVES_PATH, face_id, name, filename)
		self.trainer.train(self._SAVES_PATH)

	def set_faces_dir(self, new_dir: str):
		"""
		Set new directory with faces
		:param new_dir: new directory name
		"""
		if not os.path.isdir(new_dir):
			raise NotADirectoryError(f"{new_dir} is not a directory")
		self._SAVES_PATH = new_dir

	@property
	def camera_image_counter(self):
		return self.camera_loader.image_count

	def set_camera_image_count(self, cnt: int):
		self.camera_loader.set_image_count(cnt)


class BaseImageLoader(ABC):
	def __init__(
			self,
			scale_factor: Optional[float] = None,
			min_neighbors: Optional[int] = None,
			min_size: Optional[tuple[int, int]] = None
	):
		self._SCALE_FACTOR = scale_factor or 1.2
		self._MIN_NEIGHBORS = min_neighbors or 5
		self._MIN_SIZE = min_size or (20, 20)
		self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		self._SAVES_PATH = "faces"

	def _save_face(self, face_id: int, num: int, img: str, username: str = "user"):
		file_path = f"{self._SAVES_PATH}/{username}.{face_id}.{num}.jpg"
		cv2.imwrite(file_path, img)

	@abstractmethod
	def load(self, save_path: str, face_id: int, name: str, source: Optional[str] = None):
		pass


class CameraLoader(BaseImageLoader):
	"""
	Loading face from camera manager.
	"""
	def __init__(self, image_count=None, scale_factor=None, min_neighbors=None, min_size=None):
		super().__init__(scale_factor, min_neighbors, min_size)
		self._IMAGE_COUNT = image_count or 30

	def __str__(self):
		return "Camera Loader"

	def load(self, save_path: str, face_id: int = 0, name: str = "user", source: Optional[str] = None):
		"""
		Load face image from camera.

		Params:
			face_id: int - unique id of the user
			name: str - name of the user

		Collects self._IMAGE_COUNT different images of user's face by default.
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
				cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
				count += 1
				self._save_face(face_id, count, gray[y:y + h, x:x + w], name)

			cv2.imshow("camera", img)
			k = cv2.waitKey(100) & 0xff  # 'ESC'
			if k == 27 or count >= self._IMAGE_COUNT:
				break

		cap.release()
		cv2.destroyAllWindows()

	@property
	def image_count(self):
		return self._IMAGE_COUNT

	def set_image_count(self, cnt: int):
		"""
		Set new value of self._IMAGE_COUNT

		:param cnt: int: new count of images to take when adding a new face from camera
		"""
		if not isinstance(cnt, int):
			raise ValueError("Provide an integer value for image count")
		if not (0 < cnt <= 30):
			raise ValueError(f"{cnt} is too big number")

		self._IMAGE_COUNT = cnt


class FileLoader(BaseImageLoader):
	"""
	Loading face from file manager.
	"""
	def __init__(self, scale_factor=None, min_neighbors=None, min_size=None):
		super().__init__(scale_factor, min_neighbors, min_size)

	def __str__(self):
		return "File loader"

	def load(self, save_path: str, face_id: int = 0, name: str = "user", source: Optional[str] = None):

		"""
		Load a new face from file
		:param save_path: path to save a face picture
		:param face_id: unique id of user whose face is being saved
		:param name: new of the user
		:param source: source image with the face
		"""
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
	"""
	LBPH Face recognizer training manager.
	"""
	def __init__(self):
		pass

	def __str__(self):
		return "Trainer"

	@staticmethod
	def _get_faces_and_ids(path: str) -> tuple[list[str], list[int]]:
		"""
		:param path: a directory with saved faces pictures
		:return: two lists with face images and corresponding user ids
		"""
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
		"""
		Train a LPBH Face Recognizer and create a .yml description
		:param path: directory with faces pictures
		"""
		faces, ids = self._get_faces_and_ids(path)
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.train(faces, np.array(ids))
		recognizer.write('face.yml')
