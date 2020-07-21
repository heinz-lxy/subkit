import t 

video_id = 99
video = 'wp%s'%(video_id) 
src = r'H:\字幕君\五朋兼\%s\%s.txt'%(video,video)
dest = r'H:\字幕君\五朋兼\%s\%s-2.txt'%(video,video)
f1 = open(src,'r')
f2 = open(dest,'w')
text = f1.read()
lines = text.split('\n')
for line in lines:
    line = '\\'+line 
    f2.write(line+'\n')
f1.close()
f2.close()
t.rm(src)
t.mv(dest,src)


