from check_convertion import input_float
from decarator import timer
import math, time

@timer
def ln_approximation(x, eps):
    '''
       Evaluate function f(x) = ln((1+x)/(1-x)) with Taylor series
               :parameter:
                       x (float): in this point, function evaluate
                       eps(float): necessary accuracy
               :return
                       result(float): result of function f(x) = ln((1+x)/(1-x)) in point x
                       n(int): count of members in Taylor series
                       term(float): Obtained accuracy
    '''
    if x == 0:
        return None,None,None
    result = 0
    n = 0
    term = 2/x
    #end new member of Taylor series> accuraty
    while abs(term) > eps:
        #add new member
        result += term
        n += 1
        #evaluate new member
        term = 2 /( (2 * n + 1)* x ** (2*n+1))
        if n > 500:
            return None,None,None
    #to demonstrate the decorator
    time.sleep(1)
    return result,n,term

def Task1():
    '''
        Test function ln_approximation(x, eps)
    '''
    x = input_float("Enter x, must be |x| >1: ")
    eps = input_float("Enter accuracy: ")
    result,n,term, time1 = ln_approximation(x, eps)
    if result is None:
        print("Count of iterations >500, may be you enter x which |x| <=1")
    else:
        print(f"You entered x: {x}")
        print(f"Count of series members {n}")
        print(f"Obtained accuracy {term}")
        print(f"My result : {result}")
        print(f"Real solution : {math.log((x + 1) / (x - 1))}")
    print(f"Time: {time1} c")