import cv2
import numpy as np
import json
import t 
from threading import Thread
import time
import re

class VideoStream(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.frame = None 

    def update(self): 
        while True:
            (self.status, self.frame) = self.capture.read()

    def get_frame(self):
        return self.frame
        
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
            # sample_region = frame[604:648,134:234]
            # caption_lower = 604
            # caption_upper = 648 
            
            sample_region = cv2.cvtColor(sample_region, cv2.COLOR_BGR2GRAY)
            
            sample_region = sample_region > white_threshold  
            sample_region = sample_region < 5
            
            white_total = sample_region.sum()
            
            vertical_shape_vector = sample_region.sum(axis=1)
            horizontal_shape_vector = sample_region.sum(axis=0)

            # print(vertical_shape_vector)
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
  
            print(ratio)
            if(ratio<0.05 or ratio>0.8):
                continue 
            # if(shape_std<10 or shape_std>20):
            #     continue
            try:
                diff = self.calc_vector_distance(vertical_shape_vector, self.prev_frame)
                # print(diff)
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

    def batch_run(self):
        video_folder = r'H:\字幕君\五朋兼\#batch'
        for video in t.files(video_folder):
            if(not self.running):
                break
            if(not 'mp4' in video):
                continue
            video_path = t.path_join(video_folder,video)
            save_folder = video[:5]
            f = open("channels.txt","r",encoding="utf-8") 
            channels = json.loads(f.read())
            for channel in channels:
                if(channel['keyword'] in video):
                    self.fp = frame_processor(video_path,save_folder)
                    self.fp.gen_caption_screenshots(**channel)

    def run(self, video_ids=None):
        print(video_ids)
        video_folder = r'H:\字幕君\五朋兼'
        for video in t.files(video_folder):
            if(not self.running):
                break
            if(video_ids==None):
                if(not 'mp4' in video):
                    continue
                video_path = t.path_join(video_folder,video)
                save_folder = video[:5]
                f = open("channels.txt","r",encoding="utf-8") 
                channels = json.loads(f.read())
                for channel in channels:
                    if(channel['keyword'] in video):
                        self.fp = frame_processor(video_path,save_folder)
                        self.fp.gen_caption_screenshots(**channel)
            else:
                for video_id in video_ids:
                    if str(video_id) in video and ('mp4' in video):
                        video_path = t.path_join(video_folder,video)
                        save_folder = video[:5]
                        f = open("channels.txt","r",encoding="utf-8") 
                        channels = json.loads(f.read())
                        for channel in channels:
                            if(channel['keyword'] in video):
                                print('hi25')
                                self.fp = frame_processor(video_path,save_folder)
                                self.fp.gen_caption_screenshots(**channel)          
            
def word_capture(video_id):
    video = 'wp%s'%(video_id) 
    src = r'H:\字幕君\五朋兼\%s\%s.txt'%(video,video)
    text = open(src,'r').read()
    b = re.findall(r'([a-zA-Z]*),,',text,re.M)
    b = list(set(b))
    with open('wordlist.txt','w') as f:
        f.write(',\n'.join(b))
        f.close()
    t.open_file('wordlist.txt')

def word_replace(video_id):
    video = 'wp%s'%video_id 
    text_path = r'H:\字幕君\五朋兼\%s\%s.txt'%(video,video)
    text = open(text_path,'r').read()
    with open('wordlist.txt','r') as f:
        content = f.read()
        for line in content.split('\n'):
            try:
                old, new = line.split(',')
                text = text.replace(old+',,',new)
                text = text.replace(old,new)
            except:
                pass
    with open(text_path,'w') as f:
        f.write(text)        
        f.close()


def sub_format(video_id):
    video = 'wp%s'%(video_id) 
    src = r'H:\字幕君\五朋兼\%s\%s.txt'%(video,video)
    dest = r'H:\字幕君\五朋兼\%s\%s-2.txt'%(video,video)
    f1 = open(src,'r')
    f2 = open(dest,'w')
    text = f1.read()
    text = text.replace(" i "," I ")
    text = text.replace(" u ","you")
    text = text.replace("\nu ","\nyou ")
    text = text.replace(" r ","are")
    text = text.replace("\nr ","\nare ")
    text = text.replace(" yr "," you are ")
    text = text.replace("\nyr ","\nyou are ")
    text = text.replace("whats","what's")
    text = text.replace("dont","don't")
    text = text.replace("wont","won't")
    text = text.replace("dst","doesn't")
    text = text.replace("cant","can't")
    text = text.replace("i'm","I'm")
    text = text.replace("i'll","I'll")
    text = text.replace("i've","I've")
    text = text.replace("hv","have")
    text = text.replace("gv","give")
    text = text.replace("ft","father")
    text = text.replace("mt","mother")
    text = text.replace("remb","remember")
    text = text.replace("pls","please")
    text = text.replace("mum","Mum")
    text = text.replace("dad","Dad")
    text = text.replace("rmb","RMB")
    text = text.replace("god","God")
    import re

    tmp = ''
    for (index, block) in enumerate(text.split('\n\n')):
        if(index>0):
            tmp += '\n\n'
        tmp2 = ''
        for (index2, line) in enumerate(re.split(r'\n\s{0,}',block)):
            if(index2>0):
                tmp2 += '\n'
            line = line.strip()
            try:
                line = line[0].upper()+line[1:]
                tmp2 += line
            except:
                tmp2 += line
        tmp += tmp2 
    text = tmp

    tmp = ''
    for (index, line) in enumerate(re.split('\.\s{1,}',text)):
        if(index>0):
            tmp += '. '
        line = line.strip()
        try:
            line = line[0].upper()+line[1:]
            tmp += line
        except:
            tmp += line
    text = tmp

    tmp = ''
    for (index, line) in enumerate(re.split(r'\?[^\S\n]{1,}',text)):
        if(index>0):
            tmp += '? '
        line = line.strip()
        try:
            line = line[0].upper()+line[1:]
            tmp += line
        except:
            tmp += line
    text = tmp

    f2.write(text)

    f1.close()
    f2.close()
    t.rm(src)
    t.mv(dest,src)

def trans_int_to_digit(integer, digit):
    if(digit==2):
        if integer<10:
            return '0'+str(integer)
        else:
            return str(integer)
    if(digit==3):
        if integer<10:
            return '00'+str(integer)
        elif(integer<100):
            return '0'+str(integer)
        else:
            return str(integer)

def trans_ms_to_formal(time_ms):
    hour = int(time_ms/1000/60/60)
    minute = int(time_ms/1000/60)
    second = int(time_ms/1000%60) 
    ms = time_ms%1000
    hour = trans_int_to_digit(hour,2)
    minute = trans_int_to_digit(minute,2)
    second = trans_int_to_digit(second,2)
    ms = trans_int_to_digit(ms,3)

    return '%s:%s:%s,%s'%(hour,minute,second,ms)

def gen_srt_block(time_block, text, index):
    time_block[0] = trans_ms_to_formal(time_block[0])
    time_block[1] = trans_ms_to_formal(time_block[1])
    rst = str(index)+'\n'+' --> '.join(time_block)+'\n'+text+'\n\n'
    return rst 

def extract_marks(a):
    lines = a.split('\n')
    marks = []
    for line in lines:
        try:
            parts = line.split('/')
            marks.append({
                'text':parts[1],
                'time_block_index':parts[0].split('+')
            })
        except:
            continue
    return marks


def gen_marks(text_file):
    content = open(text_file,'r').read()
    text = ''
    for block in content.split('\n\n'):
        tmp_index = 0
        if('*' in block):
            b = re.findall(r'([0-9]*)\*([\s\S]*)\n([0-9]*)\*',block,re.M)
            index = int(b[0][0])
            block = b[0][1]
            # print(block)
            block_end = int(b[0][2])
            for block_line in block.split('\n'):
                print(block_line)
                if(tmp_index==0):
                    block_line = block_line[0].upper()+block_line[1:]
                tmp_index += 1
                if('/' in block_line):
                    x,y = block_line.split('/')
                    y = y[0].upper()+y[1:]
                    if('+' in x):
                        start, end = x.split('+')
                        text +=  x+'/'+y+'\n'
                        if(index!=int(start)):
                                raise Exception('marks wrong at index %s, block: %s'%(index,y))
                        index = int(end)+1
                    else:
                        length = int(x)
                        text += str(index)+'+'+str(index+length-1)+'/'+y+'\n'
                        index +=  length
                    continue
                block_line = block_line[0].upper()+block_line[1:]
                text += '%s/%s'%(index,block_line)+'\n'
                index +=  1
            if(index!=(block_end+1)):
                raise Exception(str(index)+'marks wrong: block end %s'%block_end)
        else:
            print(block)
            x,y = block.split('/')
            y = y[0].upper()+y[1:]
            if('+' in x):
                start, end = x.split('+')  #unfinished
                text += x+'/'+y+'\n'
                index =  int(end)+1
            else:
                text += x+'/'+y+'\n'
                index +=  int(x) +1
    return extract_marks(text)

def gen_srt(video_id):
    video_id = 'wp%s'%(video_id) 
 
    time_blocks = t.open_pickle('%s/%s.pkl' % (video_id,video_id))
    marks = gen_marks('%s/%s.txt' % (video_id,video_id))
    # print(time_blocks)
    f = open('%s/%s.srt' % (video_id,video_id),'w')
    i=0
    for mark in marks:
        text = mark['text']
        i+=1
        time_block_index = mark['time_block_index']
        if(len(time_block_index)>1):
            caption_start = time_blocks[time_block_index[0]][0]
            caption_end = time_blocks[time_block_index[1]][1]
            time_block = [caption_start, caption_end]
        else:
            time_block = time_blocks[time_block_index[0]]
        try:
            a = gen_srt_block(time_block, text, i)
        except:
            print(text)
        f.write(a)
    f.close()


