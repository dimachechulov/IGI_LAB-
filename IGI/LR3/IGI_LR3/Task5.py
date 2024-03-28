from functools import reduce

from initialization import *
from check_convertion import *


def print_multiplication_between_min_max(arr):
    '''
          Print multiplication between min and max value.
          :parameter
            arr(list): input list

    '''
    index_min = min(arr.index(max(arr)), arr.index(min(arr)))
    index_max = max(arr.index(max(arr)), arr.index(min(arr)))
    if index_min == index_max or index_max - 1 == index_min:
        print(f"0 elements between max and min el")
    elif index_max - 2 == index_min:
        multiplication = arr[index_min + 1]
        print(f"Multiplication numbers between max and min element in list: {multiplication}")
    else:
        multiplication = reduce((lambda x, y: x * y), arr[index_min + 1: index_max])
        print(f"Multiplication numbers between max and min element in list: {multiplication}")

def choise_generate_list_method(len):
    '''
          Choise which generate list method use and generate list.
          :parameter
            len(int): count of element in list
          :return
            generated list
    '''
    result = []
    while True:

        method = input_int("Enter which method, you want use to generate list(if with generator enter 1,"
                           "if with loop enter 2, if with random nubers enter 3  ): ")
        match method:
            case 1:
                result = my_generate_sequence(len)

            case 2:
                result = base_generate_sequence(len)
            case 3:
                result = genarate_random_sequence(len)
            case _:
                print("Indefined request\n")
                continue
        break
    return result


def Task5():
    '''
        Test function  choise_generate_list_method(len) and print_multiplication_between_min_max(arr) and print sum negative number.
    '''
    len = input_posint("Enter count elements in list: ")
    arr = choise_generate_list_method(len)
    print(f"Generated arr: {arr}")
    sum_negative = sum([el for el in arr if el <0])
    print(f"Sum negative numbers {sum_negative}")
    print_multiplication_between_min_max(arr)


