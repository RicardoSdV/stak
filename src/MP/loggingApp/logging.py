from multiprocessing import Queue

def interpreter2Logger(queue):  # type: (Queue) -> None
    while True:
        msg = queue.get()
        if msg == "__STOP__":
            break

        print 'From interpreter2:', msg
