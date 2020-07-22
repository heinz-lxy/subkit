from utilities import *
from gui import *

def init():
    app = App().set_size(200,400).set_loc(1000,100).set_title('subkit')

    def func(e):
        pass

    def trans_quick_scan():
        video_path = video_path_input.get()
        caption_lower = int(caption_lower_input.get())
        caption_upper = int(caption_upper_input.get())
        white_threshold = int(white_threshold_input.get())
        consistency_threshold = int(consistency_threshold_input.get())
        from threading import Thread
        global fbp
        fbp = frame_batch_processor()
        thread = Thread(target=fbp.run, args=(video_path, caption_lower, caption_upper, white_threshold, consistency_threshold))
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

    def trans_sub_format():
        video_id = input_box.get()
        sub_format(int(video_id))

    def trans_gen_srt():
        video_id = input_box.get()
        gen_srt(int(video_id))


    fbp = None
    app.label('video path').grid(row=1, column=1, padx=1)
    video_path_input = app.input(func)
    video_path_input.grid(row=1, column=2, padx=1)
    app.label('caption lower').grid(row=2, column=1, padx=1)
    caption_lower_input = app.input(func)
    caption_lower_input.grid(row=2, column=2, padx=1)
    app.label('caption upper').grid(row=3, column=1, padx=1)
    caption_upper_input = app.input(func)
    caption_upper_input.grid(row=3, column=2, padx=1)
    app.label('white threshold').grid(row=4, column=1, padx=1)
    white_threshold_input = app.input(func)
    white_threshold_input.grid(row=4, column=2, padx=1)
    app.label('consistency threshold').grid(row=5, column=1, padx=1)
    consistency_threshold_input = app.input(func)
    consistency_threshold_input.grid(row=5, column=2, padx=1)

    app.button('scan',trans_quick_scan).grid(row=7, column=1, padx=1)
    app.button('cancel scan',cancel_shot).grid(row=8, column=1, padx=1)
    app.button('word capture',trans_word_capture).grid(row=9, column=1, padx=1)
    app.button('word replace',trans_word_replace).grid(row=10, column=1, padx=1)
    app.button('format text',trans_sub_format).grid(row=11, column=1, padx=1)
    app.button('gen sub',trans_gen_srt).grid(row=12, column=1, padx=1)
    app.label('-')
    

    app.run()                 


if __name__ == '__main__':
    init()
