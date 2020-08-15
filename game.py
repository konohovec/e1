import random
import os
import sys
from functools import partial


WORDS = ['skillfactory', 'testing', 'blackbox', 'pytest', 'unittest', 'coverage']
IN_GAME = True

if os.name == 'nt':
    clear_screen = partial(os.system, 'cls')
else:
    clear_screen = partial(os.system, 'clear')


def choose_word(words):
    '''Returns a random word from the list and the same word represented by the underlines'''
    task = random.choice(words)
    word = '_' * len(task)
    return task, word


def draw(word, misses, message=''):
    '''Displays the game state'''
    clear_screen()
    print(f'misses: {misses}')
    print(' '.join(word))
    print(message, '\n')


def user_attempt():
    '''Accepts and returns user input'''
    letter = None
    while not letter:
        letter = input('Input a letter: ').lower().strip()
        if len(letter) > 1:
            letter = None
            print('You need to enter a single letter')

    return letter


def check_letter(task, word, letter, misses):
    '''Checks if the letter in a word. If not, increases the misses'''
    for i, l in enumerate(task):
        if l == letter:
            word = word[:i] + l + word[i + 1:]

    if letter not in task:
        misses += 1

    return word, misses


def game_status(word, misses):
    '''Checks if the user guessed a word or ran out of attempts'''
    global IN_GAME

    if misses >= 4:
        draw(word, misses, 'You lose. (×_×)')
        IN_GAME = False
    if '_' not in word:
        draw(word, misses, 'Congrats, you won!')
        IN_GAME = False


def main():
    task, word = choose_word(WORDS)

    misses = 0
    while IN_GAME:
        draw(word, misses)
        letter = user_attempt()
        word, misses = check_letter(task, word, letter, misses)
        game_status(word, misses)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)
