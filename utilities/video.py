import cv2
import numpy as np
import json
import t 
from threading import Thread
import time
import re

class frame_processor:
    def __init__(self, video_path, save_folder):
        self.vc = cv2.VideoCapture(video_path) 
        self.time_ms = -200
        self.prev_frame = None
        self.caption_index = 0
        self.captions_image = None
        self.captions_image_index = 0
        self.time_blocks = {}
        self.folder = save_folder
        self.running = True

        t.mkdir(self.folder)
    
    def stop(self):
        self.running = False

    def calc_vector_distance(self, v1, v2):
        return np.sqrt(np.sum(np.square(v1-v2)))

    def concat_2d_image(self, im1, im2):
        return np.concatenate([im1, im2],axis=0)
        
    def write_remaining_caption(self, time_block):
        self.time_blocks[str(self.caption_index)] = time_block
        # print('end')
        # print(time_block)
        t.save_pickle(self.folder+'/'+self.folder + '.pkl', self.time_blocks)
        cv2.imwrite(self.folder+'/'+t.timestamp() + '.jpg',self.captions_image)

    def merge_caption_image(self, caption, time_block):
        caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SIMPLEX
        captions_image = self.captions_image
        captions_image_index = self.captions_image_index
        caption_index = self.caption_index

        caption_index += 1
        self.time_blocks[str(caption_index-1)] = time_block
        cv2.putText(caption, str(caption_index), (400,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3) 
        if(captions_image_index==0):
            captions_image = np.zeros(caption.shape)
        captions_image = self.concat_2d_image(captions_image,caption)
        if(captions_image_index>18): # 3, 18
            cv2.imwrite(self.folder+'/'+t.timestamp() + '.jpg',captions_image)
            captions_image = []
            captions_image_index = 0 
        else:
            captions_image_index += 1 

        self.captions_image = captions_image
        self.captions_image_index = captions_image_index
        self.caption_index = caption_index

    def gen_caption_screenshots(self, caption_lower=634, caption_upper=689, \
        white_threshold=240,consistency_threshold =40, caption_start_time = -200, **props):
        self.time_ms = caption_start_time
        caption_start = None 
        caption_end = None 
        while self.running:  
            self.time_ms += 200
            self.vc.set(cv2.CAP_PROP_POS_MSEC, self.time_ms)
            grabbed, frame = self.vc.read()
            if not grabbed:
                caption_end = self.time_ms
                self.write_remaining_caption([caption_start,caption_end])
                break
            screen_width = frame.shape[1]
            sample_left = int(screen_width/2-(caption_upper-caption_lower))
            sample_right = int(screen_width/2+(caption_upper-caption_lower)) # sample_left = 36 # sample_right = 131
            sample_region = frame[caption_lower:caption_upper,sample_left:sample_right]
            
            sample_region = cv2.cvtColor(sample_region, cv2.COLOR_BGR2GRAY)
            
            sample_region = sample_region > white_threshold  
            sample_region = sample_region < 5
            
            white_total = sample_region.sum()
            
            vertical_shape_vector = sample_region.sum(axis=1)
            horizontal_shape_vector = sample_region.sum(axis=0)

            shape_std = np.std(vertical_shape_vector)/np.mean(vertical_shape_vector)
            if(shape_std<0.5 and shape_std>1):
                continue
            vertical_filled_rate = (vertical_shape_vector >2).sum()/len(vertical_shape_vector)
            if(vertical_filled_rate<0.7):
                continue
            horizontal_filled_rate = (horizontal_shape_vector >2).sum()/len(horizontal_shape_vector)
            if(horizontal_filled_rate<0.35):
                continue

            height, width = sample_region.shape
            area = width * height
            ratio = white_total / area
  
            if(ratio<0.05 or ratio>0.8):
                continue 
          
            try:
                diff = self.calc_vector_distance(vertical_shape_vector, self.prev_frame)
            except Exception as e:
                pass
            else:
                if(diff < consistency_threshold):
                    self.prev_frame = vertical_shape_vector
                    caption_end = self.time_ms + 200
                    continue
            caption = frame[caption_lower:caption_upper, 0:screen_width]
            self.merge_caption_image(caption, [caption_start, caption_end])
            caption_start = self.time_ms
            caption_end = self.time_ms
            caption_end = self.time_ms + 200
            self.prev_frame = vertical_shape_vector
 
class frame_batch_processor:
    def __init__(self):
        self.fp = None
        self.running = True

    def stop(self):
        self.fp.stop()
        self.running = False

    def run(self, video_path, caption_lower, caption_upper, white_threshold, consistency_threshold):
        self.fp = frame_processor(video_path,'123')
        self.fp.gen_caption_screenshots(caption_lower, caption_upper, white_threshold, consistency_threshold)
        
# from threading import Thread
# import cv2, time

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
   

