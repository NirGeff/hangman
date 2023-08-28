import os

HANGMAN_ASCII_ART = ("""welcome to the game hangman /
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/""")

MAX_TRIES = (6)

HANGMAN_PHOTOS = {"stage 0": "x-------x", "stage 1": """x-------x
|
|
|
|
|""", "stage 2": """x-------x
|       |
|       0
|
|
|""", "stage 3": """x-------x
|       |
|       0
|       |
|
|
""", "stage 4": """x-------x
|       |
|       0
|      /|\\
|
|""", "stage 5": """x-------x
|       |
|       0
|      /|\\
|      /
|""", "stage 6": """x-------x
|       |
|       0
|      /|\\
|      / \\
|"""}

def opening_screen():
    """
    the func prints the opening screen
    :return void:
    """
    print(HANGMAN_ASCII_ART, "Your number of max tries is: {}".format(MAX_TRIES), sep='\n')

def fix_path(file_path):
    """
    the funcs rempve
    :param file_path:
    :return:
    """
    if (file_path[0] == "\"" or file_path[0] == "\'") and (file_path[-1] == "\"" or file_path[-1] == "\'"):
        return file_path[1:-1]
    else:
        return file_path

def get_data_from_user():
    """
    the funcs get the path file and the index of word from the user
    :return file path - the path of file - string, the index of the word - int:
    """
    file_path_of_words = fix_path(input("Enter file path: "))
    while not os.path.exists(file_path_of_words):
        print("The path is not valid or doesn't point to a file.")
        file_path_of_words = fix_path(input("Enter file path: "))
    index_of_word = input("Enter_index: ")
    while not index_of_word.isnumeric():
        print("The index should be a number")
        index_of_word = input("Enter_index: ")
    return file_path_of_words, int(index_of_word)

def choose_word(file_path, index):
    """
    the funcs return the word in the number of the index
    :param file_path - the path of the file, str:
    :param index - the index of the word to guess, int:
    :return the word in the number of the index,string:
    """
    with open(file_path, "r") as source:
        words = source.readlines()
    words = words[0].split()
    length = len(set(words))
    real_index = int(index) % len(words)
    word = words[real_index-1]
    return word

def print_hangman(num_of_tries):
    """
    the funcs prints the hangman state according to the number of tries
    :param num_of_tries - how many times the player guessed wrong - int:
    :return - void:
    """
    print(HANGMAN_PHOTOS["stage {}".format(num_of_tries)], "\n")

def show_hidden_word(secret_word, old_letters_guessed):
    """
    the funcs prints the word the player need to guess and the letters he had already guessed
    :param secret_word - the word he needs to guess, a string:
    :param old_letters_guessed - the letters he had already guessed, a list:
    :return - the word he need to guess with the letters he had already guessed, a string:
    """
    hidden_word = ""
    for letter in secret_word:
        if letter not in old_letters_guessed:
            hidden_word += "_ "
        else:
            hidden_word += letter + " "
    return hidden_word[:-1]

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    the funcs receive the user's guess and old guesses and  add his guess to the list of guesses if the letter is one alphabetic letter.
    :param letter_guessed - the letter the user gueesed, string:
    :param old_letters_guessed - the guess he gussed before, list:
    :return if the letter is ok, boolean:
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        return True
    else:
        print("X - not a valid input, enter 1 new alphabetic letter")
        if old_letters_guessed:
            print("the letters you already guessed are:", " -> ".join(sorted(old_letters_guessed)))
        return False

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    the func tells if the letter guessed is only one alphabetic letter and was not guessed before
    :param letter_guessed - the letter we check, string:
    :param old_letter_guessed - all the letters the player already guessed, list:
    :return if the letter is valid and was not guessed before, boolean:
    """
    letter_guessed = letter_guessed.lower()
    return len(letter_guessed) == 1 and letter_guessed.isalpha() and letter_guessed not in old_letters_guessed

def check_win(secret_word, old_letters_guessed):
    """
    the funcs checks if the player won and guessed all the letters
    :param secret_word - the word he needs to guess, a string:
    :param old_letters_guessed - the letters he had already guessed, a list:
    :return - void:
    """
    return "_" not in show_hidden_word(secret_word, old_letters_guessed)

def guessing_a_letter(old_letters_guessed, secret_word, num_of_tries):
    """
    the funcs lets the player guess a letter, show him the state of the word and the state of the hangman and old
    guessed letters if he guessed wrong
    :param old_letters_guessed - all the letters he already guessed - list:
    :param secret_word - the word he needs to guess - string:
    :param num_of_tries - the number of wrong guesses - num:
    :return - the updated list of the letters he guessed - list, the updated number of wrong guesses - num:
    """
    letter_guessed = input("Guess a letter:").lower()
    while not try_update_letter_guessed(letter_guessed, old_letters_guessed): #i want to check if the letter is valid
        letter_guessed = input("Guess a letter:").lower()
    old_letters_guessed.append(letter_guessed)
    if letter_guessed not in secret_word:
        print(":(")
        num_of_tries += 1
        print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))
    return old_letters_guessed, num_of_tries

def main():
    opening_screen()
    secret_word = choose_word(*get_data_from_user())
    num_of_tries = 0
    old_letter_guessed = []
    print("\nLet's start!")
    print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letter_guessed))
    while num_of_tries < MAX_TRIES:
        old_letter_guessed, num_of_tries = guessing_a_letter(old_letter_guessed, secret_word, num_of_tries)
        if check_win(secret_word, old_letter_guessed):
            print("WIN")
            break
    if num_of_tries == MAX_TRIES:
        print("LOSE \nThe word was {}".format(secret_word.upper()))

if __name__ == "__main__":
    main()