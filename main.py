import cv2
import threading
import time
from rs_232_class import rs_232_ctl
from imutils.video import FileVideoStream

def set_flag_after_delay(flag, delay):
    flag[0] = True
    time.sleep(delay)
    flag[0] = False


class VideoPlayer:
    def __init__(self):
        self.display_controller = rs_232_ctl(verbose=False)
        self.resolution = self.display_controller.get_resolution()
        
        self.reset_screen = False
        self.pip_active = False
        self.override_TV = False
        self.ad_active = False
        
        self.notification_scale = 35
        self.pip_scale = 45

        self.screenID = {"TV": 1, "RPi": 2}

        # Set Notification Preset
        width = 16*self.notification_scale
        height = 9*self.notification_scale
        self.display_controller.set_window_layout(1)
        self.display_controller.set_window_priority(2)
        self.display_controller.set_hposition(self.screenID["RPi"], self.resolution[1]-width)
        self.display_controller.set_vposition(self.screenID["RPi"], 0)
        self.display_controller.set_height(self.screenID["RPi"], height)
        self.display_controller.set_width(self.screenID["RPi"], width)
        time.sleep(1)

        self.family_ring_cap = cv2.VideoCapture("media/video_family_comp.mp4")
        if not self.family_ring_cap.isOpened():
            print("Error: Could not open family video file.")
            exit(-1)
        

        self.ad_cap = cv2.VideoCapture("media/video_ad_comp.mkv")
        if not self.ad_cap.isOpened():
            print("Error: Could not open exercise advert video file.")
            exit(-1)

        self.exercise_ad_cap = cv2.VideoCapture("media/video_exercise_ad_comp.mkv")
        if not self.exercise_ad_cap.isOpened():
            print("Error: Could not open exercise advert video file.")
            exit(-1)

        self.exercise_pip_cap = cv2.VideoCapture("media/video_exercise_comp.mkv")
        if not self.exercise_pip_cap.isOpened():
            print("Error: Could not open exercise video file.")
            exit(-1)

        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self.welcome = [False]
        self.welcome_page = cv2.imread('media/Welcome.PNG')

        # Scenario 2 - hydration reminder
        self.hydration_reminder = [False]
        self.hydration_notification = cv2.imread('media/hydration_notification.jpeg')
        self.hydration_notification = self.resize_notification(self.hydration_notification)

        # Scenario 3 - family calling
        self.family_ringing = [False]
        self.family_answered = [False]
        self.call_notification = cv2.imread('media/call_notification.png')
        self.call_notification = self.resize_notification(self.call_notification)

        # Scenario 7 - ad break prompt during exercise
        self.exercise_ad_popup = [False]
        self.exercise_ad_full = [False]
        self.exercise_ad_reminder_set = [False]
        self.exercise_ad_notification = cv2.imread('media/exercise_ad_notification.jpg')
        self.exercise_ad_notification = self.resize_notification(self.exercise_ad_notification)
        self.exercise_ad_reminder = cv2.imread('media/exercise_ad_reminder_set.jpg')
        self.exercise_ad_reminder = self.resize_notification(self.exercise_ad_reminder)

        # Scenario 8 - pip exercise during tv programme
        self.exercise_pip_popup = [False]
        self.exercise_pip = [False]
        self.exercise_pip_reminder_set = [False]
        self.exercise_pip_notification = cv2.imread('media/exercise_pip_notification.jpg')
        self.exercise_pip_notification = self.resize_notification(self.exercise_pip_notification)
        self.exercise_pip_reminder = cv2.imread('media/exercise_pip_reminder_set.jpg')
        self.exercise_pip_reminder = self.resize_notification(self.exercise_pip_reminder)

        # Scenario 9 - Tai Chi reminder
        self.taichi_reminder = [False]
        self.taichi_acknowledge = [False]
        self.taichi_snooze = [False]
        self.taichi_notification = cv2.imread('media/taichi_notification.jpeg')
        self.taichi_notification = self.resize_notification(self.taichi_notification)
        self.taichi_acknowledge_notification = cv2.imread('media/taichi_acknowledge.jpeg')
        self.taichi_acknowledge_notification = self.resize_notification(self.taichi_acknowledge_notification)
        self.taichi_snooze_notification = cv2.imread('media/taichi_snooze.jpeg')
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

    def add_notification(self, notification):
        # Overlay the image in the top-right corner
        
        if not self.pip_active:
            #width = notification.shape[1]*self.notification_scale
            #height = notification.shape[0]*self.notification_scale
            self.display_controller.set_window_layout(1)
            #self.display_controller.set_hposition(self.screenID["RPi"], self.resolution[1]-width)
            #self.display_controller.set_vposition(self.screenID["RPi"], 0)
            #self.display_controller.set_height(self.screenID["RPi"], height)
            #self.display_controller.set_width(self.screenID["RPi"], width)
            self.pip_active = True

        return notification

    def add_ad_notification(self, frame, notification):
        # Overlay the image in the top-left corner
        frame[self.buffer:notification.shape[0]+self.buffer, frame.shape[1] - notification.shape[1] - self.buffer:frame.shape[1] - self.buffer] = notification
        return frame
        
    def add_pip(self, pip_cap):
            
        if not self.pip_active:
            #pip_cap.start()
            #width = pip_frame.shape[0]*pip_scale
            #height = pip_frame.shape[1]*self.pip_scale
            self.display_controller.set_window_layout(1)
            #self.display_controller.set_hposition(self.screenID["RPi"], self.resolution[1]-width)
            #self.display_controller.set_vposition(self.screenID["RPi"], 0)
            #self.display_controller.set_height(self.screenID["RPi"], height)
            #self.display_controller.set_width(self.screenID["RPi"], width)

            self.pip_active = True 
        
        ret, pip_frame = pip_cap.read()
        if not ret:
            pip_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, pip_frame = pip_cap.read()

        return pip_frame

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
                self.override_TV = True

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
            return None

        elif key == ord("a"):
            self.reset_flags()
            if self.ad_active:
                self.ad_active = False
                return 1
            else:
                self.ad_active = True
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
            self.display_controller.set_full_scrn_mode(2)
            exit()

        return None

    def modify_frame(self, cap, frame):
        reset = True
        
        # Scenario 2
        if self.hydration_reminder[0] is True:
            frame = self.add_notification(self.hydration_notification)
            reset = False

        # Scenario 3
        if self.family_ringing[0] is True:
            frame = self.add_notification(self.call_notification)
            reset = False

        if self.family_answered[0] is True:
            frame = self.add_pip(self.family_ring_cap)
            reset = False

        # Scenario 7
        if self.exercise_ad_popup[0] is True:
            #cap = self.ad_cap
            frame = self.add_ad_notification(frame, self.exercise_ad_notification)
            reset = False

        if self.exercise_ad_full[0] is True:
            cap = self.exercise_ad_cap
            reset = False

        if self.exercise_ad_reminder_set[0] is True:
            frame = self.add_ad_notification(frame, self.exercise_ad_reminder)
            reset = False

        # Scenario 8
        if self.exercise_pip_popup[0] is True:
            frame = self.add_notification(self.exercise_pip_notification)
            reset = False

        if self.exercise_pip[0] is True:
            frame = self.add_pip(self.exercise_pip_cap)
            reset = False

        if self.exercise_pip_reminder_set[0] is True:
            frame = self.add_notification(self.exercise_pip_reminder)
            reset = False

        # Scenario 9
        if self.taichi_reminder[0] is True:
            frame = self.add_notification(self.taichi_notification)
            reset = False

        if self.taichi_acknowledge[0] is True:
            frame = self.add_notification(self.taichi_acknowledge_notification)
            reset = False

        if self.taichi_snooze[0] is True:
            frame = self.add_notification(self.taichi_snooze_notification)
            reset = False

        # Reset if no scenarios
        if ((reset)and(self.pip_active)):
            self.reset_screen = True
        
        return cap, frame

    def play_video(self):

        # Welcome full screen
        self.display_controller.set_full_scrn_mode(2)
        cv2.imshow("Video", self.welcome_page)
        cv2.waitKey(0)
        
        self.reset_screen = True

        cap = None
        frame = None
        
        while True:
            
            if cap is not None:
                ret, frame = cap.read()

                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
            
            try:
                cap, frame = self.modify_frame(cap, frame)
            except Exception as e:
                    print(e)
            
            if frame is not None:
                cv2.imshow("Video", frame)
            # Check for key press
            key = cv2.waitKey(1)

            self.prompt_options(key)
            ret_cap = self.scenario_options(key)
            if ret_cap is not None:
                if ret_cap == 1:
                    cap = None
                    self.reset_screen = True
                else:
                    cap = ret_cap
                    self.override_TV = True

            if self.override_TV:
                # Display the frame in full screen
                self.display_controller.set_full_scrn_mode(2)
                self.override_TV = False
                
            if self.reset_screen:
                # Display the TV in full screen
                self.display_controller.set_full_scrn_mode(1)

                self.reset_screen = False
                self.pip_active = False

            

        # Release the video capture object and close the window
        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    video = VideoPlayer()
    video.play_video()
