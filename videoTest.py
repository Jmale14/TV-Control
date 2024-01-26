import cv2

cap = cv2.VideoCapture("media/video_exercise_comp.mkv")
if not cap.isOpened():
	print("Error: Could not open exercise video file.")
	exit(-1)

cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		cv2.imshow("Video", frame)
		
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		

	else:
		break

cap.release()
cv2.destroyAllWindows()
