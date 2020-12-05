from __future__ import annotations

import sys
import argparse
import os

from face_loader import FaceLoader
from authenticator import Authenticator


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
