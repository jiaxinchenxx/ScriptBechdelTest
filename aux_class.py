class Script_info(object):

    def __init__(self, Scenes, GenderDic, CharacterSet):
        self.Scenes = Scenes
        self.GenderDic = GenderDic
        self.CharacterSet = CharacterSet


class DialogueInstance(object):

    def __init__(self):
        self.Femaledialogue = []
        self.isAboutMan = []


class ScriptStatics(object):

    def __init__(self, Characters, Males, Females, dialogueInstance, canPassTest):

        self.DialogueInstance = dialogueInstance
        self.numOfFemale = len(Females)
        self.FemaleSet = Females
        self.MaleSet = Males
        self.Characters = Characters
        self.numOfInstance = len(self.DialogueInstance.Femaledialogue)

        self.canPassTest = canPassTest
