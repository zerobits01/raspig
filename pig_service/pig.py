from global_vars import tasks_queue
from time import sleep
from utils.client import get_new_tasks, get_weight, update_task_to_done

if __name__ == "__main__":
    # check everything in a while True and request every 30 mins
    # first get new task will return the pig id till we set the owner
    while True:
        try:
            resp = get_new_tasks()
            print(resp)
            for item in resp:
                if item not in tasks_queue:
                    tasks_queue.append(item)
            resp = get_weight()
            print(resp)
            while True:
                try:
                    t = tasks_queue.popleft()
                except:
                    break
                print(f"trying to update {t}")
                print(update_task_to_done(t['id']))            
            sleep(5)
        except Exception as e:
            print(f"error is {e}, lineno is {e.__traceback__.tb_lineno}")