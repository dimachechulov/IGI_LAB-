from check_convertion import input_int
import random

def my_generate_sequence(len):
    '''
       Generate list with yield and input numbers.
               :parameter:
                       len(int): len of list
               :return
                     (list): result list
    '''
    for i in range(len):
        num = input_int(f"Input arr[{i+1}]: ")
        yield num

def base_generate_sequence(len):
    '''
      Generate list with loop and input numbers.
              :parameter:
                      len(int): len of list
              :return
                    (list): result list
    '''
    my_list = []
    for i in range(len):
        my_list.append(input_int(f"Input arr[{i+1}]: "))
    return my_list

def genarate_random_sequence(len):
    '''
                  Random Generate list.
                          :parameter:
                                  len(int): len of list
                          :return
                                (list): result list
    '''
    my_list = []
    for i in range(len):
        my_list.append(random.randint(-1000,1000))

    return my_list

