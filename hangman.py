import os
import random

HANGMAN_ASCII_ART = ("""welcome to the game hangman 
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/""")

MAX_TRIES = 6

MAX_INPUT_ATTEMPTS = 2

DEFAULT_PATH = r"C:\Users\GMO\Desktop\sample.txt"

HANGMAN_PHOTOS = [r"x-------x", r"""x-------x
|
|
|
|
|""", r"""x-------x
|       |
|       0
|
|
|""", r"""x-------x
|       |
|       0
|       |
|
|
""", r"""x-------x
|       |
|       0
|      /|\
|
|""", r"""x-------x
|       |
|       0
|      /|\
|      /
|""", r"""x-------x
|       |
|       0
|      /|\
|      / \
|"""]

def print_opening_screen() -> None:
    """
    The func prints the opening screen.
    :return Void:
    """
    print(HANGMAN_ASCII_ART, f"Your number of max tries is: {MAX_TRIES}", sep="\n")

def get_path_from_user() -> str:
    """
    The funcs get a path file from the user.
    :return The file path which inclides the words to choose from - string :
    """
    for attempt in range(MAX_INPUT_ATTEMPTS + 1):
        path = input("Enter file path: ")
        path = path.strip('"\'')
        if os.path.isfile(path) and read_file(path):
            return path
        else:
            print("The path is not valid or doesn't point to a file or empty.")
    print("It seems like you are having trouble finding a path, don't worry it's alright! I will just use my deafult path :)")
    return DEFAULT_PATH

def get_index_from_user() -> int:
    """
    The funcs get the path file which includes the words and the index of word from the user.
    :return A tuple containing the file path - string and the index of the word - int.:
    """
    for attempt in range(MAX_INPUT_ATTEMPTS + 1):
        word_index = input("Enter the number of your secret word: ")
        if word_index.isnumeric():
            return word_index
        else:
            print("Be aware you write a number")
    print("It seems like you are having trouble choosing a number, don't worry it's alright! I will just pick one for u :)")
    return random.randint(1, 1000)

def read_file(path) -> list:
    """
    The funcs read the file and return all the words in it within a list.
    :param path: Str, the path of the file which contains the words.
    :return: List, the list of the words in the file.
    """
    with open(path, "r") as words_file:
        words = words_file.readlines()
    return words

def choose_word(path, index) -> str:
    """
    The funcs return the word in the number of the index.
    :param path - the path of the file which contains the words, str:
    :param index - the index of the word to guess, int:
    :return The word in the number of the index,string:
    """
    words = read_file(path)[0].split()
    index_in_bounds = index % len(words) - 1
    word = words[index_in_bounds]
    return word

def print_hangman(num_of_tries) -> None:
    """
    The funcs prints the hangman state according to the number of tries.
    :param num_of_tries - how many times the player guessed wrong - int:
    :return - Void:
    """
    print(HANGMAN_PHOTOS[num_of_tries], "\n")

def show_hidden_word(secret_word, old_letters_guessed) -> str:
    """
    The funcs prints the word the player need to guess and the letters he had already guessed.
    :param secret_word - the word he needs to guess, a string:
    :param old_letters_guessed - the letters he had already guessed, a list:
    :return - The word he need to guess with the letters he had already guessed, a string:
    """
    hidden_word = ""
    for letter in secret_word:
        if letter not in old_letters_guessed:
            hidden_word += "_ "
        else:
            hidden_word += letter + " "
    return hidden_word[:-1]

def try_update_letter_guessed(letter_guessed, old_letters_guessed) -> bool:
    """
    The funcs receive the user's guess and old guesses and  add his guess to the list of guesses if the letter is one alphabetic letter.
    :param letter_guessed - the letter the user gueesed, string:
    :param old_letters_guessed - the guess he gussed before, list:
    :return If the letter is ok, boolean:
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        return True
    else:
        print("X - not a valid input, enter 1 new alphabetic letter")
        if old_letters_guessed:
            print("the letters you have already guessed are:", " -> ".join(sorted(old_letters_guessed)))
        return False

def check_valid_input(letter_guessed, old_letters_guessed) -> bool:
    """
    The func tells if the letter guessed is only one alphabetic letter and was not guessed before.
    :param letter_guessed - the letter we check, string:
    :param old_letter_guessed - all the letters the player already guessed, list:
    :return If the letter is valid and was not guessed before, boolean:
    """
    letter_guessed = letter_guessed.lower()
    return len(letter_guessed) == 1 and letter_guessed.isalpha() and letter_guessed not in old_letters_guessed

def check_win(secret_word, old_letters_guessed) -> bool:
    """
    The funcs checks if the player won and guessed all the letters.
    :param secret_word - the word he needs to guess, a string:
    :param old_letters_guessed - the letters he had already guessed, a list:
    :return - Void:
    """
    return "_" not in show_hidden_word(secret_word, old_letters_guessed)

def guessing_a_letter(old_letters_guessed, secret_word, num_of_tries) -> tuple[list, int]:
    """
    The funcs lets the player guess a letter, show him the state of the word and the state of the hangman and old
    guessed letters if he guessed wrong.
    :param old_letters_guessed - all the letters he already guessed - list:
    :param secret_word - the word he needs to guess - string:
    :param num_of_tries - the number of wrong guesses - num:
    :return - The updated list of the letters he guessed - list, the updated number of wrong guesses - num:
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
    print_opening_screen()
    path = get_path_from_user()
    index = get_index_from_user()
    secret_word = choose_word(path, index)
    number_of_tries = 0
    previously_guessed_letters = []
    print("\nLet's start!")
    print_hangman(number_of_tries)
    print(show_hidden_word(secret_word, previously_guessed_letters))
    if_won = False
    while number_of_tries < MAX_TRIES:
        previously_guessed_letters, num_of_tries = guessing_a_letter(previously_guessed_letters, secret_word, number_of_tries)
        if check_win(secret_word, previously_guessed_letters):
            if_won = True
            break
    if if_won:
        print("WIN")
    else:
        print(f"LOSE \nThe word was {secret_word.upper()}")


if __name__ == "__main__":
    main()
