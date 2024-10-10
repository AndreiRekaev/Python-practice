import unittest
from collections import Counter
import random

# Signals:
def cooperate_step():
    return "cooperate"

def cheat_step():
    return "cheat"

# The main idea is that the first we update prev_step:
def steps(step: int, player1: object, player2: object):
    player1.update_prev_step()
    player2.update_prev_step()

    if player1.get_behaviour_type() == "detective":
        player1.check_cheat(player2)

    if player2.get_behaviour_type() == "detective":
        player2.check_cheat(player1)

    if (player1.get_behaviour_type() == "copycat") or (player1.get_behaviour_type() == "grudger"):
        player1.update_next_step(player2)
    elif player1.get_behaviour_type() == "detective":
        player1.update_next_step(step, player2)
    elif player1.get_behaviour_type() == "copykitten":
        player1.update_next_step(player2)

def result(step: int, player1: object, player2: object):
    print("----------", "ROUND №", step, "----------")
    print("     Player № 1 has:", player1.get_candies())
    print("     Player № 2 has:", player2.get_candies())

class Player(object):
    def __init__(self, behaviour_type: str = "", candies: int = 0):
        self.next_step = ""
        self.prev_step = ""
        self.behaviour_type = behaviour_type

        if candies < 0:
            self.candies = 0
        else:
            self.candies = candies


    def get_next_step(self):
        return self.next_step

    def get_prev_step(self):
        return self.prev_step

    def get_candies(self):
        return self.candies

    def change_candies(self, candies: int):
        self.candies = self.get_candies() + candies

    def get_behaviour_type(self):
        return self.behaviour_type

    def update_prev_step(self):
        self.prev_step = self.get_next_step()

class Cheater(Player):
    def __init__(self, behaviour_type: str = "cheater"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cheat_step()

    def update_next_step(self):
        self.next_step = cheat_step()

class Cooperator(Player):
    def __init__(self, behaviour_type: str = "cooperator"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cooperate_step()

    def update_next_step(self):
        self.next_step = cooperate_step()

class Copycat(Player):
    def __init__(self, behaviour_type: str = "copycat"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cooperate_step()

    def update_next_step(self, player: object):
        self.next_step = player.get_prev_step()

class Grudger(Player):
    def __init__(self, behaviour_type: str = "grudger"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cooperate_step()

    def update_next_step(self, player: object):
        if (player.get_next_step() == cheat_step()) or (self.get_next_step() == cheat_step()):
            self.next_step = cheat_step()
        else:
            self.next_step = cooperate_step()

class Detective(Player):
    def __init__(self, behaviour_type: str = "detective"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cooperate_step()
        self.cheat_flag = False

    def check_cheat(self, player: object):
        if player.get_prev_step() == cheat_step():
            self.cheat_flag = True

    def update_next_step(self, step: int, player: object):
        if step == 0:
            self.next_step = cheat_step()
        elif step in [1, 2]:
            self.next_step = cooperate_step()
        elif self.cheat_flag:
            self.next_step = player.get_prev_step()
        else:
            self.next_step = cheat_step()

class CopyKitten(Player):
    def __init__(self, behaviour_type: str = "copykitten"):
        super().__init__(behaviour_type)
        self.behaviour_type = behaviour_type
        self.next_step = cooperate_step()
        self.errors_made = 0  # Количество ошибок, сделанных противником

    def update_next_step(self, player: object):
        if player.get_prev_step() == cheat_step():
            self.errors_made += 1
            if self.errors_made > 1:
                self.next_step = cheat_step()
            else:
                self.next_step = cooperate_step()
        else:
            # Повторяем поведение CopyCat, если нет ошибки
            self.next_step = player.get_prev_step()

class Game(object):

    def __init__(self, matches=10):
        if matches < 1:
            self.matches = 1
        else:
            self.matches = matches

        self.registry = Counter()

    def top3(self):
        # print top three
        return self.registry.most_common()[0:2]

    def update_top(self, player1: object, player2: object):
        if player1.get_candies() > player2.get_candies():
            self.registry.update([player1.get_behaviour_type()])
        elif player2.get_candies() > player1.get_candies():
            self.registry.update([player2.get_behaviour_type()])

    def play(self, player1: object, player2: object):
        # simulate number of matches
        # equal to self.matches
        print("\n\nBefore the game players have:", player1.get_candies(), " - ", player2.get_candies(), end="\n\n")
        for i in range(self.matches):
            # Both cheaters:
            if (player1.get_next_step() == cheat_step()) and (player2.get_next_step() == cheat_step()):
                steps(i, player1, player2)

            # Both cooperate:
            elif (player1.get_next_step() == player2.get_next_step()) and (player1.get_next_step() == cooperate_step()):
                player1.change_candies(2)
                player2.change_candies(2)
                steps(i, player1, player2)

            # First cheater, the second cooperate
            elif player1.get_next_step() == cheat_step():
                player1.change_candies(3)
                player2.change_candies(-1)
                steps(i, player1, player2)

            else:
                player1.change_candies(-1)
                player2.change_candies(3)
                steps(i, player1, player2)

            result(i, player1, player2)

        self.update_top(player1, player2)
        print(self.top3())

if __name__ == "__main__":  # Case if we don't import module (tests)
    class TestsEx01(unittest.TestCase):

        def tests_cheater(self):
            game = Game()

            # Cheater games:
            # № 1: Cheater versus Cooperate:
            cheater = Cheater()
            cooperate = Cooperator()

            game.play(cheater, cooperate)
            self.assertEqual(cheater.get_candies(), 30)
            self.assertEqual(cooperate.get_candies(), -10)

            # № 2: Cheater versus Copycat:
            cheater = Cheater()
            copycat = Copycat()

            game.play(cheater, copycat)
            self.assertEqual(cheater.get_candies(), 30)
            self.assertEqual(copycat.get_candies(), -10)

            # № 3: Cheater vs Grudger:
            cheater = Cheater()
            grudger = Grudger()

            game.play(cheater, grudger)
            self.assertEqual(cheater.get_candies(), 30)
            self.assertEqual(grudger.get_candies(), -10)

            # № 4: Cheater versus Detective:
            cheater = Cheater()
            detective = Detective()

            game.play(cheater, detective)
            self.assertEqual(cheater.get_candies(), 30)
            self.assertEqual(detective.get_candies(), -10)

            # Cooperate games:
            # № 1: Cooperate versus Copycat:
            cooperate = Cooperator()
            copycat = Copycat()

            game.play(cooperate, copycat)
            self.assertEqual(cooperate.get_candies(), 20)
            self.assertEqual(copycat.get_candies(), 20)

            # № 2: Cooperate versus Grudger:
            cooperate = Cooperator()
            grudger = Grudger()

            game.play(cooperate, grudger)
            self.assertEqual(cooperate.get_candies(), 20)
            self.assertEqual(grudger.get_candies(), 20)

            # № 3: Cooperate versus Detective:
            cooperate = Cooperator()
            detective = Detective()

            game.play(cooperate, detective)
            self.assertEqual(cooperate.get_candies(), 20)
            self.assertEqual(detective.get_candies(), 20)

            # # Copycat games:
            # № 1: Copycat versus Detective:
            copycat = Copycat()
            detective = Detective()

            game.play(copycat, detective)
            self.assertEqual(copycat.get_candies(), 20)
            self.assertEqual(detective.get_candies(), 20)

            # № 2: Copycat vs Grudger:
            copycat = Copycat()
            grudger = Grudger()

            game.play(copycat, grudger)
            self.assertEqual(copycat.get_candies(), 20)
            self.assertEqual(grudger.get_candies(), 20)

            # Grudger games:
            # № 1: Grudger versus Detective:
            grudger = Grudger()
            detective = Detective()

            game.play(grudger, detective)
            self.assertEqual(grudger.get_candies(), 20)
            self.assertEqual(detective.get_candies(), 20)

        def tests_top(self):
            game = Game()
            grudger = Grudger()

            # One top:
            cheater = Cheater()
            cooperator = Cooperator()

            game.play(cheater, cooperator)
            self.assertEqual(game.top3(), [("cheater", 1)])

            # Two tops:
            detective = Detective()

            game.play(cooperator, detective)
            game.play(grudger, detective)
            game.play(cheater, detective)
            game.play(cheater, cooperator)
            self.assertEqual(game.top3(), [("cheater", 3), ("detective", 2)])

        # Final test for all difference pairs:
        # def tests_final(self):
        #     game = Game()
        #     cooperate = Cooperator()
        #     copycat = Copycat()
        #     grudger = Grudger()
        #     cheater = Cheater()
        #     detective = Detective()

        #     game.play(cheater, cooperate)
        #     game.play(cheater, copycat)
        #     game.play(cheater, grudger)
        #     game.play(cheater, detective)
        #     game.play(cooperate, copycat)
        #     game.play(cooperate, grudger)
        #     game.play(cooperate, detective)
        #     game.play(copycat, detective)
        #     game.play(copycat, grudger)
        #     game.play(grudger, detective)
        #     self.assertEqual(game.top3(), [('cheater', 4), ('cooperator', 2)])

        # Tests for bonus part (top 2 after cheater):
        # def tests_bonus(self):
        #     game = Game()
        #     cheater = Cheater()
        #     cooperate = Cooperator()
        #     copycat = Copycat()
        #     grudger = Grudger()
        #     detective = Detective()
        #     copykitten = CopyKitten()

        #     game.play(copykitten, cheater)
        #     game.play(copykitten, cooperate)
        #     game.play(copykitten, copycat)
        #     game.play(copykitten, grudger)
        #     game.play(copykitten, detective)
        #     self.assertEqual(game.top3(), [("copykitten", 4), ("cheater", 1)])

    
    unittest.main()
