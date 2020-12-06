from __future__ import annotations

import sys
import argparse
import os

from face_loader import FaceLoader
from authenticator import Authenticator


class EmptyDirectoryName(Exception):
	pass


class AppManager:
	def __init__(self):
		self.loader = FaceLoader()
		self.authenticator = Authenticator()

		self.__set_faces_dir('faces')

	def load_from_camera(self, face_id, name):
		return self.loader.load_from_camera(face_id, name)

	def load_from_file(self, filename: str, face_id, name):
		return self.loader.load_from_file(filename, face_id, name)

	def authenticate(self):
		return self.authenticator.authenticate()

	def get_next_face_id(self) -> int:
		try:
			return max(map(int, [filename.split('.')[1] for filename in os.listdir(self.__faces_dir)]))
		except IndexError:
			return 0

	def __set_faces_dir(self, dir_name: str = 'faces'):
		if not os.path.isdir(dir_name):
			os.mkdir(dir_name)
		self.__faces_dir = dir_name

	@property
	def faces_dir(self):
		return self.__faces_dir

	def set_faces_dir(self, new_dir: str):
		if not os.path.isdir(new_dir):
			raise NotADirectoryError(f"{new_dir} is not a directory")

		self.loader.set_faces_dir(new_dir)
		self.authenticator.set_faces_dir(new_dir)

	@property
	def confidence_threshold(self):
		return self.authenticator.confidence_threshold

	def set_confidence_threshold(self, th: int):
		self.authenticator.set_confidence_threshold(th)

	@property
	def camera_image_count(self):
		return self.loader.camera_image_counter

	def set_camera_image_count(self, cnt: int):
		self.loader.set_camera_image_count(cnt)
