import cv2
import numpy as np
import t 

class frame_processor:
    def __init__(self):
        self.video_folder = r'H:\字幕君\五朋兼\$视频'
        self.output_image = None
        self.output_index = 0
        self.shot_index = 0
        self.time_blocks = {}
        self.time_ms = -200

    def calc_vector_distance(self, v1, v2):
        return np.sqrt(np.sum(np.square(v1-v2)))

    def concat_two_dimension_image(self, im1, im2):
        return np.concatenate([im1, im2],axis=0)
        
    def write_remaining_caption(self, save_path, time_block):
        self.time_blocks[str(shot_index)] = time_block
        t.save_pickle(save_path+'\\'+save_path + '.pkl', self.time_blocks)
        cv2.imwrite(save_path+'\\'+t.timestamp() + '.jpg',output_image)

    def merge_caption_image(self, caption, save_path, time_block):
        caption = cv2.cvtColor(caption, cv2.COLOR_BGR2GRAY)
        font=cv2.FONT_HERSHEY_SIMPLEX
        shot_index += 1
        time_blocks[str(shot_index-1)] = time_block
        cv2.putText(caption, str(shot_index), (400,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3) 
        if(output_index==0):
            output_image = np.zeros(caption.shape)
        output_image = concat_two_dimension_image(output_image,caption)
        if(output_index>18): # 3, 18
            cv2.imwrite(save_path+'\\'+t.timestamp() + '.jpg',output_image)
            output_image = []
            output_index = 0 
        else:
            output_index += 1 

    def gen_video_caption_screenshot(self, folder, caption_lower=634, caption_upper=689, \
        white_threshold=240,consistency_threshold =30, start_time = -200, **props):
        vc = cv2.VideoCapture(self.video_path) 
        prev = None
        time_ms = start_time
        start = None 
        end = None 
        
        while True:  
            self.time_ms += 200
            vc.set(cv2.CAP_PROP_POS_MSEC,time_ms)
            state, frame = vc.read()
            try:
                screen_width = frame.shape[1]
            except:
                end = time_ms
                write_remaining_caption(folder,[start,end])
                break
            sample_left = int(screen_width/2-(caption_upper-caption_lower))
            sample_right = int(screen_width/2+(caption_upper-caption_lower)) # sample_left = 36 # sample_right = 131
            sample_region = frame[caption_lower:caption_upper,sample_left:sample_right]
            sample_region = cv2.cvtColor(sample_region, cv2.COLOR_BGR2GRAY)
            sample_region = sample_region > white_threshold  
            white_total = sample_region.sum()

            white_bar = sample_region.sum(axis=1)

            height, width = sample_region.shape
            area = width * height
            ratio = white_total / area
            # print(ratio)
            if(ratio<0.05 or ratio>0.8):
                continue 
            try:
                diff = calc_vector_distance(white_bar,prev)
                print(diff)
                if(diff>consistency_threshold):    ### change, mostly 39
                    output = frame[caption_lower:caption_upper, 0:screen_width]
                    merge_caption_image(output,folder,[start, end]) 
                    start = time_ms
                    end = time_ms + 200
            except:
                end = time_ms
                output = frame[caption_lower:caption_upper, 0:screen_width]
                merge_caption_image(output,folder,[start, end])
                start = time_ms
                prev = white_bar
            end = time_ms + 200
            prev = white_bar