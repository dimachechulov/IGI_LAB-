def count_words_start_with_lower_letter(s):
    '''
           Calculate count words in input string, which starts with lower letter.
           :parameter
                s(str): input string
            :return
                res(int):  count words
    '''
    words =s.split()
    res = 0
    for word in words:
        for char in word:
            #
            if not char.isalpha():
                continue
            elif char.islower():
                res+=1
            break
    return res

def Task3():
    '''
           Test function count_words_start_with_lower_letter(s)
    '''
    s = input("Enter string, in which you want to count words start with lower letter: ")
    print(f"Count words start with lower letter: {count_words_start_with_lower_letter(s)}")
