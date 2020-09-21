#!/usr/bin/env python3

from __future__ import annotations

import sys
import argparse

import face_loader
import face_recognizer
import face_authenticator


class Application:	
	
	"""
	singleton
	
	
	self.face_loader = face_loader.FaceLoader()  # face loading app
	self.face_recognizer = face_recognizer.FaceRecognizer()  # face recognition module
	self.face_authenticator = face_authenticator.FaceAuthenticator()  # face authentication app
	
	
	self.__bindings: Dict[Class] = {"app_name": application}
		e.g. self.bingings["loader"] = self.face_loader
	
	"""
	
	def __init__(self, cmd=None):
		# self.run(cmd)
		
		self.face_loader = face_loader.FaceLoader()
		self.face_recognizer = face_recognizer.FaceRecognizer()
		self.face_authenticator = face_authenticator.FaceAuthenticator()
		
		self.bindings = {
			"loader": self.face_loader,
			"recognizer": self.face_recognizer,
			"authenticator": self.face_authenticator
		}
		
	def run(self, cmd: str=None):
		self.bindings[cmd].run()
		
	


if __name__ == '__main__':
	
	app = Application()
	
	
	while True:
		app.run(input())
	
