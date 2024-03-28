import time

def timer(func):
    '''
        Decarator, which evaluate execution time.
                :parameter:
                        func (function): original  function
                :return
                        wrapper(function):updated function
    '''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return *result, end_time - start_time
    return wrapper