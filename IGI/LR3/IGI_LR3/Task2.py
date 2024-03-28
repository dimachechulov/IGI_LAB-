from check_convertion import input_int


def Task2():
    '''
        Takes integers and calculates the arithmetic mean of even numbers.
    '''
    result = 0
    count = 0
    while True:
        num = input_int("Enter next num(1 end the program): ")
        if num == 1:
            break
        elif num % 2 == 0:
            result += num
            count +=1
    if count == 0:
        print("You entered 0 even numbers")
    else:
        print (f"Result: {result / count:.4f}")