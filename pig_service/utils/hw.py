from collections import deque
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from global_vars import tasks_queue
from configs import language
from time import sleep
from utils.client import get_new_tasks, get_point, update_task_to_done, get_new
import threading
from gtts import gTTS
from playsound import playsound

pig_initialized = False

B1 = 31
B2 = 33
B3 = 35
B4 = 37
L1 = 32
L2 = 36
L3 = 38
L4 = 40

def text_to_speech(txt):
    myobj = gTTS(text=txt, lang=language, slow=False)
    myobj.save("txt.mp3")
    playsound("txt.mp3")
    print(f'from text to speech: {txt}')


def calc_leds_count(all_on):
    global tasks_queue
    l1 = l2 = l3 = l4 = False
    if all_on:
        return (True, True, True, True,)
    if len(tasks_queue) > 0:
        t = tasks_queue[0]  
        all_tasks_count = len(t['tasks'])
        done_tasks_count= len(list(
            filter(lambda a: a == True, t['tasks'].values())
        ))
        ans = done_tasks_count/all_tasks_count
        l1 = True if ans >= 0.25 else False
        l2 = True if ans >= 0.50 else False
        l3 = True if ans >= 0.75 else False
        l4 = True if ans >= 0.85 else False
    
        return (l1, l2, l3, l4)
    else:
        return (False, False, False, False)


def turn_on_leds(all_on=False):
    l1, l2, l3, l4 = calc_leds_count(all_on)
    GPIO.output(L1, GPIO.HIGH if l1 else GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH if l2 else GPIO.LOW)
    GPIO.output(L3, GPIO.HIGH if l3 else GPIO.LOW)
    GPIO.output(L4, GPIO.HIGH if l4 else GPIO.LOW)
    sleep(5)
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)
    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L4, GPIO.LOW)


def update_queue():
    global pig_initialized
    global tasks_queue
    resp = get_new_tasks()
    print(f'from update_queue: {resp}')
    if 'msg' in resp:
        text_to_speech(resp['msg'])
        return
    else:
        pig_initialized = True
    tasks_queue = deque([])
    for item in resp:
        tasks_queue.append(item)


def get_new_task_callback(channel):
    global pig_initialized
    print("get_new_task")
    update_queue()
    print(f'from get_new_task_callback: taskqueue is: {tasks_queue}')
    to_read = "there is no tasks to do, please rest!"
    if pig_initialized:
        if len(tasks_queue) > 0:
            t = tasks_queue[0]
            for k, v in t['tasks'].items():
                if v is True:
                    continue
                else:
                    to_read = k
                    break
        text_to_speech(to_read)
        # turn_on_leds()
        threading.Thread(target=turn_on_leds, args=()).start()


def get_point_callback(channel):
    if pig_initialized:
        print("get_point")
        resp = get_point()
        print(resp) 
        text_to_speech(resp['msg'])
        # turn_on_leds()
        threading.Thread(target=turn_on_leds, args=()).start()
        
    else:
        text_to_speech('pig is not initialzed, please check the id with the first button')


def set_newtask_callback(channel):
    if pig_initialized:
        print("set new task")
        resp = get_new()
        print(resp) 
        text_to_speech(resp['msg'])
        # turn_on_leds()
        threading.Thread(target=turn_on_leds, args=()).start()
        
    else:
        text_to_speech('pig is not initialzed, please check the id with the first button')


def task_done_callback(channel):
    print("task_done")
    all_on = False
    try:
        if len(tasks_queue) > 0:
            t = tasks_queue.popleft()
            temp_vals = [*t['tasks'].values()]
            if temp_vals.count(False) == 1:
                all_on = True
            print(f"trying to update {t}")
            resp = update_task_to_done(t['id'])
            print(resp)
            # turn_on_leds(t, all_on=all_on)
            update_queue()
            text_to_speech(resp['msg'])
            threading.Thread(target=turn_on_leds, args=(all_on,)).start()
        else:
            text_to_speech("there is no task to mark as done!")
    except:
        pass
    

def add_button_cbs():
    GPIO.add_event_detect(B1,GPIO.RISING,callback=get_new_task_callback, bouncetime=750)
    GPIO.add_event_detect(B2,GPIO.RISING,callback=get_point_callback, bouncetime=750)
    GPIO.add_event_detect(B3,GPIO.RISING,callback=task_done_callback, bouncetime=750)
    GPIO.add_event_detect(B4,GPIO.RISING,callback=set_newtask_callback, bouncetime=750)


def setup_pins():
    GPIO.setup(B1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(B2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(B3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(B4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(L1, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup(L2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L4, GPIO.OUT, initial=GPIO.LOW)


def setup_rasp():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    setup_pins()
    add_button_cbs()


def cleanup():
    GPIO.cleanup() # Clean up