#!/usr/bin/env python3

from __future__ import annotations

import sys
import argparse

from face_loader import FaceLoader
from authenticator import Authenticator


class AppManager:
	def __init__(self):
		self.loader = FaceLoader()
		self.authenticator = Authenticator()

	def load_from_camera(self, face_id, name):
		return self.loader.load_from_camera(face_id, name)

	def load_from_file(self, filename: str, face_id, name):
		return self.loader.load_from_file(filename, face_id, name)

	def authenticate(self):
		return self.authenticator.authenticate()

