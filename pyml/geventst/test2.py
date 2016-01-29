import gevent
import random 

def task(pid):
    gevent.sleep(0.5)
#     gevent.sleep(random.randint(0, 2)*0.001)
    print 'Task %s done' % pid
    
def synchronous():
    for i in range(10):
        task(i)
        
def asynchronous():
    threads = [gevent.spawn(task, i) for i in range(25)]
    gevent.joinall(threads)
    
# print 'Synchronous'
# synchronous()

print 'Asynchronous'
asynchronous()