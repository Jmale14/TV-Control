import cv2
import threading
import time


def set_flag_after_delay(flag, delay):
    flag[0] = True
    time.sleep(delay)
    flag[0] = False


class VideoPlayer:
    def __init__(self):
        self.tv_cap = cv2.VideoCapture("video_tv.mkv")
        if not self.tv_cap.isOpened():
            print("Error: Could not open TV video file.")
            exit(-1)

        self.family_ring_cap = cv2.VideoCapture("video_family.mp4")
        if not self.family_ring_cap.isOpened():
            print("Error: Could not open family video file.")
            exit(-1)

        self.ad_cap = cv2.VideoCapture("video_ad.mkv")
        if not self.ad_cap.isOpened():
            print("Error: Could not open exercise advert video file.")
            exit(-1)

        self.exercise_ad_cap = cv2.VideoCapture("video_exercise_ad.mkv")
        if not self.exercise_ad_cap.isOpened():
            print("Error: Could not open exercise advert video file.")
            exit(-1)

        self.exercise_pip_cap = cv2.VideoCapture("video_exercise.mkv")
        if not self.exercise_pip_cap.isOpened():
            print("Error: Could not open exercise video file.")
            exit(-1)

        # Get the video width and height
        self.width = int(self.tv_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.tv_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.welcome = [False]
        self.welcome_page = cv2.imread('Welcome.PNG')

        # Scenario 2 - hydration reminder
        self.hydration_reminder = [False]
        self.hydration_notification = cv2.imread('hydration_notification.jpeg')
        self.hydration_notification = self.resize_notification(self.hydration_notification)

        # Scenario 3 - family calling
        self.family_ringing = [False]
        self.family_answered = [False]
        self.call_notification = cv2.imread('call_notification.png')
        self.call_notification = self.resize_notification(self.call_notification)

        # Scenario 7 - ad break prompt during exercise
        self.exercise_ad_popup = [False]
        self.exercise_ad_full = [False]
        self.exercise_ad_reminder_set = [False]
        self.exercise_ad_notification = cv2.imread('exercise_ad_notification.jpg')
        self.exercise_ad_notification = self.resize_notification(self.exercise_ad_notification)
        self.exercise_ad_reminder = cv2.imread('exercise_ad_reminder_set.jpg')
        self.exercise_ad_reminder = self.resize_notification(self.exercise_ad_reminder)

        # Scenario 8 - pip exercise during tv programme
        self.exercise_pip_popup = [False]
        self.exercise_pip = [False]
        self.exercise_pip_reminder_set = [False]
        self.exercise_pip_notification = cv2.imread('exercise_pip_notification.jpg')
        self.exercise_pip_notification = self.resize_notification(self.exercise_pip_notification)
        self.exercise_pip_reminder = cv2.imread('exercise_pip_reminder_set.jpg')
        self.exercise_pip_reminder = self.resize_notification(self.exercise_pip_reminder)

        # Scenario 9 - Tai Chi reminder
        self.taichi_reminder = [False]
        self.taichi_acknowledge = [False]
        self.taichi_snooze = [False]
        self.taichi_notification = cv2.imread('taichi_notification.jpeg')
        self.taichi_notification = self.resize_notification(self.taichi_notification)
        self.taichi_acknowledge_notification = cv2.imread('taichi_acknowledge.jpeg')
        self.taichi_acknowledge_notification = self.resize_notification(self.taichi_acknowledge_notification)
        self.taichi_snooze_notification = cv2.imread('taichi_snooze.jpeg')
        self.taichi_snooze_notification = self.resize_notification(self.taichi_snooze_notification)

        self.buffer = 20

    def resize_notification(self, notification):
        return cv2.resize(notification, (notification.shape[1] // 3, notification.shape[0] // 3))

    def reset_flags(self):
        self.hydration_reminder = [False]

        self.family_ringing = [False]
        self.family_answered = [False]

        self.exercise_ad_popup = [False]
        self.exercise_ad_full = [False]
        self.exercise_ad_reminder_set = [False]

        self.exercise_pip_popup = [False]
        self.exercise_pip = [False]
        self.exercise_pip_reminder_set = [False]

        self.taichi_reminder = [False]
        self.taichi_acknowledge = [False]
        self.taichi_snooze = [False]

    def add_notification(self, frame, notification):
        # Overlay the image in the top-left corner
        frame[self.buffer:notification.shape[0]+self.buffer, frame.shape[1] - notification.shape[1] - self.buffer:frame.shape[1] - self.buffer] = notification
        return frame

    def add_pip(self, frame, pip_cap):
        ret, pip_frame = pip_cap.read()
        if not ret:
            pip_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, pip_frame = pip_cap.read()

        pip_frame = cv2.resize(pip_frame, (self.width // 4, self.height // 4))
        frame[self.buffer:pip_frame.shape[0]+self.buffer, frame.shape[1] - pip_frame.shape[1] - self.buffer:frame.shape[1] - self.buffer] = pip_frame
        return frame

    def prompt_options(self, key):

        if key == ord("y"):
            if self.family_ringing[0] is True:
                self.family_ringing[0] = False
                # Plays the family video for 10 seconds
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.family_answered, 10))
                timer_thread.start()

            if self.exercise_ad_popup[0] is True:
                self.exercise_ad_popup[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_ad_full, 10))
                timer_thread.start()

            if self.exercise_pip_popup[0] is True:
                self.exercise_pip_popup[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_pip, 10))
                timer_thread.start()

            if self.taichi_reminder[0] is True:
                self.taichi_reminder[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.taichi_acknowledge, 3))
                timer_thread.start()

        elif key == ord("n"):
            if self.family_ringing[0] is True:
                self.family_ringing[0] = False

            if self.exercise_ad_popup[0] is True:
                self.exercise_ad_popup[0] = False

            if self.exercise_pip_popup[0] is True:
                self.exercise_pip_popup[0] = False

        elif key == ord("s"):
            if self.exercise_ad_popup[0] is True:
                self.exercise_ad_popup[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_ad_reminder_set, 2))
                timer_thread.start()

            elif self.exercise_pip_popup[0] is True:
                self.exercise_pip_popup[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_pip_reminder_set, 2))
                timer_thread.start()

            elif self.taichi_reminder[0] is True:
                self.taichi_reminder[0] = False
                timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.taichi_snooze, 3))
                timer_thread.start()

    def scenario_options(self, key):
        if key == ord("p"):
            self.reset_flags()
            return self.tv_cap

        elif key == ord("a"):
            self.reset_flags()
            return self.ad_cap

        elif key == ord("2"):
            timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.hydration_reminder, 5))
            timer_thread.start()

        elif key == ord("3"):
            timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.family_ringing, 10))
            timer_thread.start()

        elif key == ord("7"):
            timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_ad_popup, 10))
            timer_thread.start()

        elif key == ord("8"):
            timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.exercise_pip_popup, 10))
            timer_thread.start()

        elif key == ord("9"):
            timer_thread = threading.Thread(target=set_flag_after_delay, args=(self.taichi_reminder, 10))
            timer_thread.start()

        elif key == ord("x"):
            exit()

        return None

    def modify_frame(self, cap, frame):
        # Scenario 2
        if self.hydration_reminder[0] is True:
            frame = self.add_notification(frame, self.hydration_notification)

        # Scenario 3
        if self.family_ringing[0] is True:
            frame = self.add_notification(frame, self.call_notification)

        if self.family_answered[0] is True:
            frame = self.add_pip(frame, self.family_ring_cap)

        # Scenario 7
        if self.exercise_ad_popup[0] is True:
            cap = self.ad_cap
            frame = self.add_notification(frame, self.exercise_ad_notification)

        if self.exercise_ad_full[0] is True:
            cap = self.exercise_ad_cap

        if self.exercise_ad_reminder_set[0] is True:
            frame = self.add_notification(frame, self.exercise_ad_reminder)

        # Scenario 8
        if self.exercise_pip_popup[0] is True:
            frame = self.add_notification(frame, self.exercise_pip_notification)

        if self.exercise_pip[0] is True:
            frame = self.add_pip(frame, self.exercise_pip_cap)

        if self.exercise_pip_reminder_set[0] is True:
            frame = self.add_notification(frame, self.exercise_pip_reminder)

        # Scenario 9
        if self.taichi_reminder[0] is True:
            frame = self.add_notification(frame, self.taichi_notification)

        if self.taichi_acknowledge[0] is True:
            frame = self.add_notification(frame, self.taichi_acknowledge_notification)

        if self.taichi_snooze[0] is True:
            frame = self.add_notification(frame, self.taichi_snooze_notification)

        return cap, frame

    def play_video(self):

        cv2.imshow("Video", self.welcome_page)
        cv2.waitKey(0)

        cap = self.tv_cap

        while True:
            ret, frame = cap.read()

            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            cap, frame = self.modify_frame(cap, frame)

            # Display the frame in full screen
            cv2.imshow("Video", frame)

            # Check for key press
            key = cv2.waitKey(1)

            self.prompt_options(key)

            ret_cap = self.scenario_options(key)
            if ret_cap is not None:
                cap = ret_cap

        # Release the video capture object and close the window
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    video = VideoPlayer()
    video.play_video()
