import pickle 
import t 

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

def extract_marks(text_file):
    file = open(text_file,'r')
    a = file.read()
    lines = a.split('\n')
    marks = []
    for line in lines:
        try:
            parts = line.split('\\')
            marks.append({
                'text':parts[1],
                'time_block_index':parts[0].split(',')
            })
        except:
            continue
    return marks

def gen_srt(id):
    time_blocks = t.open_pickle('%s\\%s.pkl' % (id,id))
    marks = extract_marks('%s\\%s.txt' % (id,id))
    f = open('%s\\%s.srt' % (id,id),'w')
    # print(marks)
    i=0
    for mark in marks:
        text = mark['text']
        i+=1
        print(i)
        time_block_index = mark['time_block_index']
        if(len(time_block_index)>1):
            start = time_blocks[time_block_index[0]][0]
            # print(time_block_index[1])
            end = time_blocks[time_block_index[1]][1]
            time_block = [start, end]
        else:
            time_block = time_blocks[time_block_index[0]]
        # a = gen_srt_block(time_block, text, index)
        try:
            a = gen_srt_block(time_block, text, i)
        except:
            print(text)
        f.write(a)
    f.close()

if __name__ == '__main__':
    gen_srt('wp93')