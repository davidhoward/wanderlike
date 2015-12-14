import random

import combatant

MAX_NUTRITION = 2500
MAX_WATER = 50

class SkillSet(object):
    def __init__(self, skill_names=[]):
        self.skills = {}
        for name in skill_names:
            self.add_skill(name)

    def add_skill(self, name):
        self.skills[name] = 0

    def get_skill(self, name):
        return self.skills.get(name, 0)

    def roll_skill(self, name):
        val = self.get_skill(name)
        if val == 0:
            return 0
        else:
            return 2 + random.randrange(val) + random.randrange(val)
        
class Character(object):
    def __init__(self, name, stats):
        # needs
        self.nutrition = MAX_NUTRITION
        self.water = MAX_WATER
        self.fatigue = 0
        # skills
        self.skills = SkillSet()
        # persona
        self.name = name
        # inventory
        # combat stats
        self.stats = combatant.Combatant(stats)
