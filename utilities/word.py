def word_capture(video_id):
    video = 'wp%s'%(video_id) 
    src = r'H:\字幕专家\%s\%s.txt'%(video,video)
    text = open(src,'r').read()
    b = re.findall(r'([a-zA-Z]*),,',text,re.M)
    b = list(set(b))
    with open('wordlist.txt','w') as f:
        f.write(',\n'.join(b))
        f.close()
    t.open_file('wordlist.txt')

def word_replace(video_id):
    video = 'wp%s'%video_id 
    text_path = r'H:\字幕专家\%s\%s.txt'%(video,video)
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
    src = r'H:\字幕专家\%s\%s.txt'%(video,video)
    dest = r'H:\字幕专家\%s\%s-2.txt'%(video,video)
    f1 = open(src,'r')
    f2 = open(dest,'w')
    text = f1.read()、
    pairs =[
        [" i "," I "],
        [" u ","you"],
        ["\nu ","\nyou "],
        [" r ","are"],
        ["\nr ","\nare "],
        [" yr "," you are "],
        ["\nyr ","\nyou are "],
        ["whats","what's"],
        ["dont","don't"],
        ["wont","won't"],
        ["dst","doesn't"],
        ["cant","can't"],
        ["i'm","I'm"],
        ["i'll","I'll"],
        ["i've","I've"],
        ["hv","have"],
        ["gv","give"],
        ["ft","father"],
        ["mt","mother"],
        ["remb","remember"],
        ["pls","please"],
        ["mum","Mum"],
        ["dad","Dad"],
        ["rmb","RMB"],
        ["god","God"]
    ]
    for pair in pairs:
        text = text.replace(pair[0],pair[1])
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