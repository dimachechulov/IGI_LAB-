def erase_dots_comma(s):
    '''
       Split string in list of words  and erase , and . in words.
       :parameter
            s(str): input string
        :return
            words(list):  result words
    '''
    words = s.split()
    for i in range(len(words)):
        if words[i][-1] == '.' or words[i][-1] == ',':
            words[i] = words[i][:-1]
    return words

def print_count_words(words):
    '''
           Print count of words in list of words.
           :parameter
            words(list): input words
    '''
    print(f"Count words: {len(words)}")

def print_count_max_word(words):
    '''
       Print biggest word in list of words.
       :parameter
         words(list): input words
    '''
    word = max(words, key=lambda x: len(x))
    index = words.index(word)
    print(f"The bigest word in text: {word}\n index: {index+1}")

def print_every_noeven_word(words):
    '''
           Print every even word.
           :parameter
             words(list): input words
    '''
    print(f"Noeven words: ")
    for i in range(len(words)):
        if (i+1) % 2 == 1:
            print(words[i], end = ' ')


def Task4():
    '''
       Test functions print_every_noeven_word(words), print_count_max_word(words), print_count_max_word(words).
    '''
    s = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    words = erase_dots_comma(s)
    print(f'Input string: {s}')
    print_count_words(words)
    print_count_max_word(words)
    print_every_noeven_word(words)
