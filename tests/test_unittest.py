import os
import sys
import io
import random
import unittest
from unittest.mock import patch
from parameterized import parameterized

sys.path.append(os.path.abspath('.'))
import game


class NullStdout:
    '''Dump'''

    def write(self, trash):
        pass


class TestChooseWord(unittest.TestCase):

    def setUp(self):
        self.words = ['word', 'word1', 'word02', 'word003']
        self.seed = random.randint(0, 100)

    def testTaskWordFromList(self):
        random.seed(self.seed)
        test_word = random.choice(self.words)

        random.seed(self.seed)
        result_word, _ = game.choose_word(self.words)
        self.assertEqual(result_word, test_word)

    def testUnderlineLength(self):
        random.seed(self.seed)
        line_length = len(random.choice(self.words))

        random.seed(self.seed)
        _, word_line = game.choose_word(self.words)
        self.assertEqual(line_length, len(word_line))


class TestCheckLetter(unittest.TestCase):

    def setUp(self):
        self.task = 'someword'
        self.word = '_' * len(self.task)
        self.misses = 0

    def testLetterExists(self):
        word, misses = game.check_letter(self.task, self.word, 'o', self.misses)
        expected_word = '_o___o__'
        with self.subTest():
            self.assertEqual(word, expected_word)
        with self.subTest():
            self.assertEqual(misses, self.misses)

    def testLetterDoesNotExist(self):
        word, misses = game.check_letter(self.task, self.word, 'x', self.misses)
        expected_word = '_' * len(self.task)
        expected_misses = 1
        with self.subTest():
            self.assertEqual(word, expected_word)
        with self.subTest():
            self.assertEqual(misses, expected_misses)


class TestUserAttempt(unittest.TestCase):

    def testCapitalLetterWithSpaces(self):
        user_input = ' B  '
        excpected_letter = 'b'

        with patch('builtins.input', side_effect=user_input):
            letter = game.user_attempt()

        self.assertEqual(letter, excpected_letter)


class TestGameStatus(unittest.TestCase):

    word = '_______'
    win_word = 'winword'

    @parameterized.expand([(word, 4), (word, 5), (word, 10), (word, 99)])
    def testRunOutOfAttemps(self, w, m):
        game.IN_GAME = True

        with patch('sys.stdout', new=NullStdout()):
            with patch('game.clear_screen', new=self.patch_clear):
                game.game_status(w, m)

        self.assertEqual(game.IN_GAME, False)

    def testGuessedWord(self):
        game.IN_GAME = True

        with patch('sys.stdout', new=NullStdout()):
            with patch('game.clear_screen', new=self.patch_clear):
                game.game_status(self.win_word, 3)

        self.assertEqual(game.IN_GAME, False)

    def testGameContinues(self):
        game.IN_GAME = True

        with patch('sys.stdout', new=NullStdout()):
            with patch('game.clear_screen', new=self.patch_clear):
                game.game_status('wo_d', 3)

        self.assertEqual(game.IN_GAME, True)

    def patch_clear(self):
        pass


class TestDraw(unittest.TestCase):

    def setUp(self):
        self.misses = random.randint(0, 4)
        self.expected_output = f'misses: {self.misses}\nw o r d\nmessage \n\n'
        self.capture = io.StringIO()

    def testOutput(self):
        with patch('sys.stdout', new=self.capture) as stdout:
            with patch('game.clear_screen', new=self.patch_clear):
                game.draw('word', self.misses, 'message')
        self.assertEqual(stdout.getvalue(), self.expected_output)

    def patch_clear(self):
        pass


if __name__ == '__main__':
    unittest.main()
