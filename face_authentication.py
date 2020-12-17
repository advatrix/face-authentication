from __future__ import annotations

import sys
import argparse
import os

from face_loader import FaceLoader, EmptyImageError, FaceNotFoundError
from authenticator import Authenticator


class EmptyDirectoryName(Exception):
	pass


class AppManager:
	"""
	The main class of the application.
	Provides API for interacting with external applications, such as GUI or CLI.
	"""
	def __init__(self):
		self.loader = FaceLoader()
		self.authenticator = Authenticator()

		self.__set_faces_dir('faces')

	def load_from_camera(self, face_id: int, name: str):
		"""
		Load a new face from the camera.
		:param face_id: unique integer id of the user
		:param name: username
		"""
		return self.loader.load_from_camera(face_id, name)

	def load_from_file(self, filename: str, face_id: int, name: str):
		"""
		Load a new face from the file.
		:param filename: source file name
		:param face_id: unique integer id of the user
		:param name: username
		"""
		return self.loader.load_from_file(filename, face_id, name)

	def authenticate(self):
		"""
		Start authentication.
		"""
		return self.authenticator.authenticate()

	def get_next_face_id(self) -> int:
		"""
		Get next available id of a new face.
		Call this method to get id for a new user.
		:return: id: int: id for a new user
		"""
		if not os.listdir(self.__faces_dir):
			return 0
		try:
			return max(map(int, [filename.split('.')[1] for filename in os.listdir(self.__faces_dir)])) + 1
		except IndexError:
			return 0

	def __set_faces_dir(self, dir_name: str = 'faces'):
		if not os.path.isdir(dir_name):
			os.mkdir(dir_name)
		self.__faces_dir = dir_name

	@property
	def faces_dir(self) -> str:
		"""
		Get current directory name where the application searches for the face pictures
		:return: str: directory name
		"""
		return self.__faces_dir

	def set_faces_dir(self, new_dir: str):
		"""
		Set a new directory name where the application will search for the face pictures
		"""
		if not os.path.isdir(new_dir):
			raise NotADirectoryError(f"{new_dir} is not a directory")

		self.loader.set_faces_dir(new_dir)
		self.authenticator.set_faces_dir(new_dir)

	@property
	def confidence_threshold(self) -> int:
		return self.authenticator.confidence_threshold

	def set_confidence_threshold(self, th: int):
		self.authenticator.set_confidence_threshold(th)

	@property
	def camera_image_count(self) -> int:
		"""
		Get current camera shot count needed to take while loading a new face from the camera
		"""
		return self.loader.camera_image_counter

	def set_camera_image_count(self, cnt: int):
		"""
		Set a new camera shot count needed to take while loading a new face from the camera
		:param cnt: a new camera shot count
		"""
		self.loader.set_camera_image_count(cnt)

	@property
	def fps(self) -> int:
		"""
		Get current camera FPS
		"""
		return self.authenticator.fps

	def set_fps(self, fps: int):
		"""
		Set new camera FPS
		"""
		self.authenticator.set_fps(fps)

	def camera_off(self):
		"""
		Turn the camera off and quit authentication mode
		"""
		self.authenticator.camera_off()

	@property
	def scale_factor(self) -> float:
		"""
		Get current scale factor of the Authenticator's classifier
		"""
		return self.authenticator.scale_factor

	@property
	def min_neighbors(self) -> int:
		"""
		Get current min neighbors parameter of the Authenticator's classifier
		"""
		return self.authenticator.min_neighbors

	@property
	def min_size(self) -> tuple[int, int]:
		"""
		Get current min size parameter of the Authenticator's classifier
		"""
		return self.authenticator.min_size

	def set_scale_factor(self, scale_factor: float):
		"""
		Set new scale factor of the Authenticator's classifier
		:param scale_factor: new scale factor
		"""
		self.authenticator.set_scale_factor(scale_factor)

	def set_min_neighbors(self, min_neighbors: int):
		"""
		Set new min neighbors parameter of the Authenticator's classifier.
		:param min_neighbors: new min neighbors count
		"""
		self.authenticator.set_min_neighbors(min_neighbors)

	def set_min_size(self, min_size_x: int, min_size_y: int):
		"""
		Set new minimum size of the image parameter of the Authenticator's classifier
		:param min_size_x: minimum width
		:param min_size_y: minimum height
		"""
		self.authenticator.set_min_size((min_size_x, min_size_y))
