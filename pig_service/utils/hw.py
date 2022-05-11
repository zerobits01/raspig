from collections import deque
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from global_vars import tasks_queue
from configs import language
from time import sleep
from utils.client import get_new_tasks, get_point, update_task_to_done
from gtts import gTTS
from playsound import playsound


def text_to_speech(txt):
    myobj = gTTS(text=txt, lang=language, slow=False)
    myobj.save("txt.mp3")
    playsound("txt.mp3")


def calc_leds_count(all_on):
    l1 = l2 = l3 = l4 = False    
    if len(tasks_queue) > 0:
        t = tasks_queue[0]
        all_tasks_count = len(t['tasks'])
        done_tasks_count= len(list(
            filter(lambda a: a == True, t['tasks'].values())
        ))
        ans = done_tasks_count/all_tasks_count
        l1 = True if ans >= 0.25 or all_on else False
        l2 = True if ans >= 0.50 or all_on else False
        l3 = True if ans >= 0.75 or all_on else False
        l4 = True if ans >= 0.85 or all_on else False
    
    return (l1, l2, l3, l4)


def turn_on_leds(all_on=False):
    l1, l2, l3, l4 = calc_leds_count(all_on)
    GPIO.output(21, GPIO.HIGH if l1 else GPIO.LOW)
    GPIO.output(22, GPIO.HIGH if l2 else GPIO.LOW)
    GPIO.output(23, GPIO.HIGH if l3 else GPIO.LOW)
    GPIO.output(24, GPIO.HIGH if l4 else GPIO.LOW)
    sleep(5)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)


def update_queue():
    resp = get_new_tasks()
    print(resp)
    tasks_queue = deque([])
    for item in resp:
        tasks_queue.append(item)


def get_new_task_callback(channel):
    sleep(0.5)
    print("get_new_task")
    update_queue()
    print(tasks_queue) # TODO: read next task
    to_read = "there is no tasks to do, please rest!"
    if len(tasks_queue) > 0:
        t = tasks_queue[0]
        for k, v in t['tasks'].items():
            if v is True:
                continue
            else:
                to_read = k
    text_to_speech(to_read)
    turn_on_leds()


def get_point_callback(channel):
    sleep(0.5)
    print("get_point")
    resp = get_point()
    print(resp) 
    text_to_speech(resp['msg'])
    turn_on_leds()


def task_done_callback(channel):
    sleep(0.5)
    print("task_done")
    all_on = False
    try:
        if len(tasks_queue) > 0:
            t = tasks_queue.popleft()
            if all(t['tasks'].values()):
                all_on = True
            print(f"trying to update {t}")
            resp = update_task_to_done(t['id'])
            print(resp)
            text_to_speech(resp['msg'])
            update_queue()
        else:
            text_to_speech("there is no task to mark as done!")
        turn_on_leds(all_on=all_on)
    except:
        pass
    

def add_button_cbs():
    GPIO.add_event_detect(8,GPIO.RISING,callback=get_new_task_callback)
    GPIO.add_event_detect(10,GPIO.RISING,callback=get_point_callback)
    GPIO.add_event_detect(12,GPIO.RISING,callback=task_done_callback)


def setup_pins():
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)


def setup_rasp():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    setup_pins()
    add_button_cbs()


def cleanup():
    GPIO.cleanup() # Clean up