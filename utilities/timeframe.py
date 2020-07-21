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