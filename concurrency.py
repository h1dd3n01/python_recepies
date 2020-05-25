'''
    You need code that can be used for concurrent operations of execution.
    Most common way to do so is trough threading library.

    import time
    def countdown(n):
        while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

    from threading import Thread
    t = Thread(target=countdown, args=(10,))
    t.start()

    t will not start unless you call start() on it.
    Processes are processed like any other usual processes despite the OS.
    Windows has its own process handling way, UNIX its own.
    You can check weather the process is still running by calling
    if t.is_alive():
        print('Still running')
    else:
        print('Completed')

    Processes can be joined by calling join() on a thread.
    Sending request for finishing a process can be a hard job of coordination, if control flow is
    trying to finishing a blocking operation request like I/O. For example, if a flow is blocked for
    a unknown time limit due to I/O it can never return. In order to make all work out, set a timeout.

    class IOTask:
        def terminate(self):
            self._running = False


        def run(self, sock):
            sock.settimeout(5)
            while self._running:
                try:
                    data = sock.recv(8192)
                    break
                except socket.timeout:
                    continue
            return
'''

'''
    Your program has a few data flows and you want to them to able to communicate with each other.
    You can use built in Queue library and make it common to each other.
    
    def producer(out_q):
        while True:
            out_q.put(data)
    
    def consumer(in_q):
        while True:
            data = in_q.get()
            
    Create a so called shared component
    q = Queue()
    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=producer, args=(q,))
    t1.start()
    t2.start()
    
    ------------------------------------------------------------------------------------
    
    from queue import Queue
    from threading import Thread
    Object that signals when job finishes
    _sentinel = object()
    
    def producer(out_q):
        while running:
            out_q.put(data)
        Put the guard in queue in order to signal when job is dome
        out_q.put(_sentinel)

    def consumer(in_q):
        while True:
            data = in_q.get()
    # Checks for the object to finish job
            if data is _sentinel:
                in_q.put(_sentinel)
                break
'''


'''
    Using threads you want to block critical parts of your program in order to avoid race conditions
    
    import threading
    
    class SharedCounter:
        # Counter class that can be common for few threads
        
        def __init__(self, initial_value=0):
            self._value = initial_value
            self._value_lock = threading.lock()
            
        def incr(self, delta=1):
            # increments counter lock value
            self._value += delta
            
        def decr(self, delta=1):
            with self._value_lock:
                self._value -= delta
                
                
    Lock guarantees common exceptions of using instructions within 'with' - that means, that only one
    thread is allowed to use instructions within 'with' block.
    
    
'''
































































