from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):

    def get_positive_effects(self):
        effects = self.base.get_positive_effects().copy()
        effects.append(type(self).__name__)
        return effects

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        effects = self.base.get_negative_effects().copy()
        effects.append(type(self).__name__)
        return effects


class Berserk(AbstractPositive):

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["HP"] += 50
        self.stats["Strength"] += 7
        self.stats["Perception"] -= 3
        self.stats["Endurance"] += 7
        self.stats["Charisma"] -= 3
        self.stats["Intelligence"] -= 3
        self.stats["Agility"] += 7
        self.stats["Luck"] += 7
        return self.stats


class Blessing(AbstractPositive):

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] += 2
        self.stats["Perception"] += 2
        self.stats["Endurance"] += 2
        self.stats["Charisma"] += 2
        self.stats["Intelligence"] += 2
        self.stats["Agility"] += 2
        self.stats["Luck"] += 2
        return self.stats


class Weakness(AbstractNegative):

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 4
        self.stats["Endurance"] -= 4
        self.stats["Agility"] -= 4
        return self.stats


class EvilEye(AbstractNegative):

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Luck"] -= 10
        return self.stats


class Curse(AbstractNegative):

    def get_stats(self):
        self.stats = self.base.get_stats()
        self.stats["Strength"] -= 2
        self.stats["Perception"] -= 2
        self.stats["Endurance"] -= 2
        self.stats["Charisma"] -= 2
        self.stats["Intelligence"] -= 2
        self.stats["Agility"] -= 2
        self.stats["Luck"] -= 2
        return self.stats
