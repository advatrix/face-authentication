import cv2


class Authenticator:
	def __init__(self):
		print("I am a face authenticator -_-")
		self.cap = cv2.VideoCapture(0)
			
	def __str__(self):
		return "Face authenticator"
		
	def run(self):
		while True:
			ret, img = self.cap.read()
			cv2.imshow("camera", img)
			if cv2.waitKey(10) == 27:
				break
		self.cap.release()
		cv2.DestroyAllWindows()

	def authenticate(self):
		self.run()
