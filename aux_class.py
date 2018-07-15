# This file provide with the auxiliary classes that are needed in the processing of scripts

# Script_info:
#   Scenes, in which would be Conversations among Characters
#   GenderDic, keys: 'female', 'male', 'unknown'. in GenderDic['female'], there are names of Female Characters, etc.
#   CharacterSet, Stores all Characters in the scripts


class Script_info(object):

    def __init__(self, Scenes, GenderDic, CharacterSet):
        self.Scenes = Scenes
        self.GenderDic = GenderDic
        self.CharacterSet = CharacterSet


# DialogueInstance:
#   Femaledialogue, stores all the instances that two females are talking to each other
#   isAboutMan,     stores whether these two females are talking about a man or not in this instance

class DialogueInstance(object):

    def __init__(self):
        self.Femaledialogue = []
        self.isAboutMan = []

# ScriptStatics:
#   DialogueInstance,   just the instance of class DialogueInstance
#   numOfFemale,        how many Females are there in this script
#   FemaleSet,          Female Characters in this script
#   MaleSet,            Male Characters in this script
#   Characters,         Characters in this script
#   numOfInstance,      How many dialogues between two females characters are there in this script
#   canPassTest,        Whether this script could pass the Bechdel Test or not

class ScriptStatics(object):

    def __init__(self, Characters, Males, Females, dialogueInstance, canPassTest):

        self.DialogueInstance = dialogueInstance
        self.numOfFemale = len(Females)
        self.FemaleSet = Females
        self.MaleSet = Males
        self.Characters = Characters
        self.numOfInstance = len(self.DialogueInstance.Femaledialogue)

        self.canPassTest = canPassTest