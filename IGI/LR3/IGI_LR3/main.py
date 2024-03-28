from Task1 import Task1
from Task2 import Task2
from Task3 import Task3
from Task4 import Task4
from Task5 import Task5
from check_convertion import input_int

def main():
    '''
        Main function, the point of entry into the program.
    '''
    print(
        "Lab 3 Chechulov group 253505\nTask 1: Сalculating the value of a function through a Taylor series with a given accuracy\n"
        "Task2: Organize a loop that takes integers and calculates the arithmetic mean of even numbers. End - input 1\n"
        "Task3: In a string entered from the keyboard, count the number of words starting with a lowercase letter\n"
        "Task4: a) determine the number of words in a line; b) find the longest word and its serial number; c) print every odd word\n"
        "Task5: Find the sum of the negative elements of a list and the product of the elements located between the maximum and minimum elements\n")
    while True:
        method = input_int(
            "If you want to test Task1 enter 1\nIf you want to test Task2 enter 2\nIf you want to test Task3 enter 3\n"
            "If you want to test Task4 enter 4\nIf you want to test Task5 enter 5\nIf you want to exit program enter -1\n")
        match method:
            case 1:
                Task1()
            case 2:
                Task2()
            case 3:
                Task3()
            case 4:
                Task4()
            case 5:
                Task5()
            case -1:
                break
            case _:
                print("Indefined request\n")



if __name__ == "__main__":
    main()




