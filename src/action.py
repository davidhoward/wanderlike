class Action(object):
    def __init__(self, name, target=None, effect=None):
        self.name = name
        if target is None and effect is None:
            raise ArgumentError("Action '%s' specified neither target nor effect" % name)
        self.target = target
        self.effect = effect

    def __call__(self, game):
        if effect is None:
            return self.target, []
        else:
            mode, msgs = self.effect(game)
            msgs.extend(game.get_status_messages())
            return mode, msgs
