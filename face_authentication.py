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
