from utils.hw import setup_rasp, cleanup

if __name__ == "__main__":
    # check everything in a while True and request every 30 mins
    # first get new task will return the pig id till we set the owner
    try:
        setup_rasp()
        while True:
            pass
    except:
        cleanup()
