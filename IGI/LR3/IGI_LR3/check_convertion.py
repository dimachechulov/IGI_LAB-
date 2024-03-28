def is_float(x):
    '''
           Check can convert str to float number or not.
                   :parameter:
                           x (str): original string
                   :return
                           (bool):  can convert str to float
           '''
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def is_int(x: str)->bool:
    '''
       Check can convert str to int number or not.
               :parameter:
                       x (str): original string
               :return
                       (bool):  can convert str to int
    '''
    try:
        b = int(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


def input_int(output_message=""):
    '''
       Input int number by checking the input.
               :parameter:
                       output_message (str): output message in console
               :return
                       (int):  input number
        '''
    s = input(output_message)
    while True:
        if is_int(s):
            break
        else:
            s = input(f"Impossible convert {s} to int, enter another value: ")
    return int(s)

def input_float(output_message="")->float:
    '''
       Input float number by checking the input.
               :parameter:
                       output_message (str): output message in console
               :return
                       (float):  input number
    '''
    s = input(output_message)
    while True:
        if is_float(s):
            break
        else:
            s = input(f"Impossible convert {s} to float, enter another value: ")
    return float(s)

def input_posint(output_message=""):
    '''
       Input positive int number by checking the input.
               :parameter:
                       output_message (str): output message in console
               :return
                       (int):  input number
        '''
    while True:
        num = input_int(output_message)
        if num <= 0:
            num = input_int("You must be positive number, try again: ")
        else:
            break
    return num




