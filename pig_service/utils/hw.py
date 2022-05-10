from collections import deque
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from global_vars import tasks_queue
from configs import language
from time import sleep
from utils.client import get_new_tasks, get_weight, update_task_to_done
from gtts import gTTS
from playsound import playsound


def text_to_speech(txt):
    myobj = gTTS(text=txt, lang=language, slow=False)
    myobj.save("txt.mp3")
    playsound("txt.mp3")
    

def turn_on_leds():
    t = tasks_queue[0]
    GPIO.output(21, GPIO.HIGH if t['t1_done'] else GPIO.LOW)
    GPIO.output(22, GPIO.HIGH if t['t2_done'] else GPIO.LOW)
    GPIO.output(23, GPIO.HIGH if t['t3_done'] else GPIO.LOW)
    GPIO.output(24, GPIO.HIGH if t['t4_done'] else GPIO.LOW)
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
    turn_on_leds()
    print(tasks_queue) # TODO: read next task


def get_weight_callback(channel):
    sleep(0.5)
    print("get_weight")
    resp = get_weight()
    turn_on_leds()
    print(resp) # TODO: read it loud using text_to_speech


def task_done_callback(channel):
    sleep(0.5)
    print("task_done")
    try:
        t = tasks_queue.popleft()
        print(f"trying to update {t}")
        print(update_task_to_done(t['id']))
        update_queue()
        turn_on_leds()
    except:
        pass
    

def add_button_cbs():
    GPIO.add_event_detect(8,GPIO.RISING,callback=get_new_task_callback)
    GPIO.add_event_detect(10,GPIO.RISING,callback=get_weight_callback)
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