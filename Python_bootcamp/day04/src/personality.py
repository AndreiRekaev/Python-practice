import random  # Module for randomized value of traits
import unittest  # Module for testing

def turrets_generator():
    traits = list()
    traits.append(random.randrange(0, 100))
    traits.append(random.randrange(0, 100 - traits[0]))
    traits.append(random.randrange(0, 100 - traits[0] - traits[1]))
    traits.append(random.randrange(0, 100 - traits[0] - traits[1] - traits[2]))
    traits.append(100 - traits[0] - traits[1] - traits[2] - traits[3])

    yield type("Turret", (),
               {
                   "neuroticism": traits[0],
                   "openness": traits[1],
                   "conscientiousness": traits[2],
                   "extraversion": traits[3],
                   "agreeableness": traits[4],

                   "shoot": lambda: print("Shooting"),
                   "search": lambda: print("Searching"),
                   "talk": lambda: print("Talking")
               })

class TestStringMethods(unittest.TestCase):
    def tests(self):
        for i in range(10):
            stanley = next(turrets_generator())

            self.assertEqual(stanley.neuroticism + stanley.openness + stanley.conscientiousness
                             + stanley.extraversion + stanley.agreeableness, 100)


    def tests_methods(self):
        stanley = next(turrets_generator())

        stanley.talk()
        stanley.search()
        stanley.shoot()

if __name__ == "__main__":
    unittest.main()