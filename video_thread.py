from threading import Thread
import cv2, time

class VideoStream(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.time_ms = 0
        self.frames = {}

    def update(self): 
        while True:
            self.capture.set(cv2.CAP_PROP_POS_MSEC, self.time_ms)
            (self.status, self.frame) = self.capture.read()
            break
            self.time_ms += 200

    def get_frame(self):
        return self.frame
   
if __name__ == '__main__':
    video_stream = VideoStream(r'H:\字幕君\五朋兼\$视频\1\wp149老公不在家，胖妹秘制荷叶鸡，鲜嫩多汁，手抱着啃得满嘴油，过瘾！【陈说美食】.mp4')
    while True:
        frame =  video_stream.get_frame()
        time.sleep(200)