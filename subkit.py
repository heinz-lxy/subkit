from SubUtility import frame_batch_processor 
from SubUtility import sub_format, word_capture, word_replace, gen_srt
from gui import *

def run():
    app = App().set_size(200,250).set_loc(1000,100).set_title('sub tool')

    def search(e):
        choice = menu.curselection()
        choice = choice[0] if choice else 0
        db = databases[choice]
        print(db)
        keyword = input_box.get()
        print(keyword)

    def trans_sub_format():
        video_id = input_box.get()
        sub_format(int(video_id))

    def trans_gen_srt():
        video_id = input_box.get()
        gen_srt(int(video_id))

    def trans_batch_shots():
        from threading import Thread
        global fbp
        fbp = frame_batch_processor()
        print('hi')
        thread = Thread(target=fbp.batch_run, args=())
        thread.daemon = True
        thread.start()

    def trans_tune_shots():
        value = input_box.get()
        video_id = []
        if ',' in value:
            video_id = value.split(',')
            video_id = list(map(lambda x:int(x),video_id)) 
        else:  
            video_id = [int(value)]

        from threading import Thread
        global fbp
        fbp = frame_batch_processor()
        thread = Thread(target=fbp.run, args=([video_id]))
        thread.daemon = True
        thread.start()

    def cancel_shot():
        global fbp  
        fbp.stop()

    def trans_word_replace():
        video_id = input_box.get()
        word_replace(int(video_id))

    def trans_word_capture():
        video_id = input_box.get()
        word_capture(int(video_id))

        
    fbp = None
    input_box = app.input(search)
    # app.label('white threshold')
    # app.input(search)
    # app.label('consistency')
    # app.input(search)
    app.button('batch shots',trans_batch_shots)
    app.button('tune shot',trans_tune_shots)
    app.button('cancel shot',cancel_shot)
    app.button('word capture',trans_word_capture)
    app.button('word replace',trans_word_replace)
    app.button('format text',trans_sub_format)
    app.button('gen sub',trans_gen_srt)
    # app.label('-')
    

    #设置截图参数 字幕输出数量 开始时间 参数
    #输出显示区

    app.run()                 


if __name__ == '__main__':


    run()
    # word_replace(172)
    # gen_srt(172)
    # fp = frame_processor()
    # fp.run()

      