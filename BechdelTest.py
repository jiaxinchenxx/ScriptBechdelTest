from nltk import RegexpTokenizer
from DialoguesReader import ScriptReader
from aux_class import DialogueInstance, ScriptStatics
import codecs
import os

FemaleFeatures = ['mrs', 'miss', 'ms', 'girl', 'woman', 'lady', 'tress', 'madam', 'mother', 'mom', 'mommy', 'munt', 'tess','cess']
MaleFeatures = ['mr', 'man', 'boy', 'gentleman', 'sir', 'father', 'dad', 'daddy', 'uncle']

auxFeatures = ['he', 'his', 'guy']

sentTokenizer = RegexpTokenizer(r'[A-Za-z]+')

savePath = '.\\'
saveName = 'Scripts.pkl'
statisticsPath = '.\Statistics'

def countFemaleofScene(scene, FemaleDic):
    '''
    :param scene: A conversation among Characters
    :param FemaleDic: The females set of the current scripts
    :return: how many Females in this conversation, who are they and the dialogues between them
    '''

    femaleCnt, instances = set(), []
    i = 0

    while i < len(scene):
        dialogue = scene[i]
        if dialogue[0] in FemaleDic and i + 1 < len(scene): # found a female Character
            femaleCnt.add(dialogue[0])

            cnt = i + 1

            FemaleA = dialogue[0]
            FemaleB = scene[cnt][0] # see who is this female talking to

            # make sure the person who talk to each other are not the same person and all of them are Females
            if FemaleA != FemaleB and FemaleA not in FemaleB and FemaleB not in FemaleA and scene[cnt][0] in FemaleDic:

                # Record the dialogues until meet a male or the end of the scene

                femaleDialogue = []
                femaleDialogue.append(dialogue)

                while cnt < len(scene) and scene[cnt][0] in FemaleDic:
                    femaleDialogue.append(scene[cnt])
                    cnt += 1

                instances.append(femaleDialogue)
                i = cnt

        i += 1

    if scene[-1][0] in FemaleDic: femaleCnt.add(scene[-1][0])

    return len(femaleCnt), femaleCnt, instances

def checkMaleExistence(dialogue, MaleDic):
    '''
    :param dialogue: the dialogues between to Female Characters
    :param MaleDic: the Male Character in this Script
    :return:
    '''

    entities = sentTokenizer.tokenize(dialogue)

    for entity in entities:

        if entity[0].isupper():
            if entity.upper() in MaleDic:
                return True

        # MaleFeatures and auxFeatures could be viewed on the top of the code, which are just naively set
        # the word like Mr, he, his, him, man, boy, etc. to identify the Male identity.
        if entity.lower() in MaleFeatures or entity.lower() in auxFeatures:
            return True

    return False


# This parser parse all the Statistics information of the scripts
class ScriptParser(object):

    def __init__(self, savename = saveName):

        self.ScriptMap = {}  # Map the scripts to their statistics
        self.savePath = savePath # savePath is the pickle file I pre-processed for you.
                                 # I would highly recommend you to use that file, cause re-process it will
                                 # take too much time

        self.Scripts = ScriptReader(10) # please input the same number you entered for num_scripts the DialoguesReader.py
        self.Scripts.loadScriptDic(self.savePath, savename) # load the pre-processed file

        self.files = self.Scripts.files # get the file names


    def parseScripts(self):

        for filename in self.Scripts.scriptDic.keys():#self.files:

            print 'Parsing ' + filename

            script = self.Scripts.scriptDic[filename]  # get the Scenes, GenderDic and CharacterSet of the script
            Scenes, GenderDic, CharacterSet = script.Scenes, script.GenderDic, script.CharacterSet

            conversationInstance = DialogueInstance()



            for i, scene in enumerate(Scenes):
                if scene != []:
                    #print 'Scene, {}:'.format(i)

                    cnt, Female, instances = countFemaleofScene(scene, GenderDic['female']) # Check if there are Female Dialogues

                    if len(instances) != 0: # If there are Female Dialogues
                        for j, instance in enumerate(instances): # For each instance of the Female Dialogues,
                            conversationInstance.Femaledialogue.append( # Store them into a DialogueInstance instance
                                ('Scene, {}'.format(i), 'Instance, {}'.format(j), instance, Female, cnt))
                            #print 'Instance, {}:'.format(j)
                            #for dialogue in instance:
                            #    print dialogue

            # save the statistics of Female dialogues for each script
            self.ScriptMap[filename] = ScriptStatics(CharacterSet, GenderDic['male'],
                                                     GenderDic['female'], conversationInstance, False)

    def parseForman(self):

        for filename in self.Scripts.scriptDic.keys():

            # this function parse each Script, with their DialogueInstance
            print 'Parsing ' + filename + ' and looking for dialogues between 2 women not about man'

            # get the DialogueInstance of each Script
            conversationInstance = self.ScriptMap[filename].DialogueInstance

            # take every instance
            for instance in conversationInstance.Femaledialogue:
                FLAG = False
                print 'Processing, ' + instance[0] + '/' + instance[1]

                # for each dialogue in this instance, check the Male existence
                for dialogue in instance[2]:
                    check = checkMaleExistence(dialogue[1], self.ScriptMap[filename].MaleSet)
                    if check: # if there is something about man, then break
                        conversationInstance.isAboutMan.append(True)
                        FLAG = True
                        break
                if not FLAG: # if there's nothing about a man, then it passes the Bechdel Test
                    conversationInstance.isAboutMan.append(False)
                    self.ScriptMap[filename].canPassTest = True

        self.parseman = True

    def printStatics(self, filename, seeDialogues = False):

        # This function performs simple statistics printing

        if filename not in self.ScriptMap.keys():
            print 'Please input a valid filename!'
            return

        scriptStatics = self.ScriptMap[filename]
        print 'Characters: ', scriptStatics.Characters
        print
        print 'Females, Total # of Female Characters: ', scriptStatics.numOfFemale
        print scriptStatics.FemaleSet
        print
        print 'Males, ', scriptStatics.MaleSet
        print

        print '# of Dialogues between women: ', scriptStatics.numOfInstance

        if self.parseman: # if we have parsed the Male information, then we could print the statistics that whether
                            # this script passes the Test or not
            print 'Could pass the test? ', scriptStatics.canPassTest

        else:
            print "Haven't parsed the information About man yet."

        print

        if seeDialogues:  # if True, then it will print all the Dialogues that between two Female Characters

            conversationInstance = scriptStatics.DialogueInstance
            for i, instance in enumerate(conversationInstance.Femaledialogue):
                print instance[0] + '/' + instance[1]
                if self.parseman:
                    print 'Contains things About man? ', conversationInstance.isAboutMan[i]

                for dialogue in instance[2]:
                    print dialogue
                print

    def printStaticsFiles(self, files, seeDialogues  = False):

        for filename in files: # print the statistics of specific files

            if filename not in self.ScriptMap.keys():
                print 'Invalid filename, ', filename, 'Skip.'
                continue

            print 'Processing file: ', filename
            self.printStatics(filename, seeDialogues)
            print '==========================================================================================='


    def writeStatistics(self):

        # function to write the Statistics to the file, which is basically the same as before

        for filename in self.files:
            print 'Writing statistics of ' + filename
            with codecs.open(os.path.join(statisticsPath, filename), 'w', encoding='utf-8') as f:

                scriptStatics = self.ScriptMap[filename]

                f.write('Statistics of ' + filename + '\n')
                f.write('All Characters: ' + '\n')
                for ac in scriptStatics.Characters:
                    f.write(ac + ', ')
                f.write('\n')
                f.write('\n')
                f.write('Females, Total # of Female Characters: ' + '  ' + str(scriptStatics.numOfFemale) + '\n')
                for fc in scriptStatics.FemaleSet:
                    f.write(fc + ', ')
                f.write('\n')
                f.write('\n')
                f.write('Males: ' + '\n')
                for mc in scriptStatics.MaleSet:
                    f.write(mc + ', ')
                f.write('\n')
                f.write('\n')

                f.write('# of Dialogues between women: ' + ' ' + str(scriptStatics.numOfInstance) + '\n')

                if self.parseman:
                    f.write('Could pass the test?' + '  ' + str(scriptStatics.canPassTest) + '\n')
                else:
                    f.write("Haven't parsed man yet. No indication about whether could pass the test or not." + '\n')

                f.write('\n')
                f.write('Instances of dialogues between females: ' + '\n')
                conversationInstance = scriptStatics.DialogueInstance
                for i, instance in enumerate(conversationInstance.Femaledialogue):

                    f.write(instance[0] + '/' + instance[1] + ' ')
                    if self.parseman:
                        f.write('Contains something about a man? ' + ' ' + str(conversationInstance.isAboutMan[i]) + '\n')
                    else:
                        f.write('\n')

                    for dialogue in instance[2]:
                        f.write(dialogue[0] + ': ' + dialogue[1])
                        f.write('\n')

                    f.write('\n')



if __name__ == '__main__':

    parser = ScriptParser(saveName) # initialize the parser with the pickle files, you could also pass a parameter which is your own
                            # savename from the DialoguesReader.py

    parser.parseScripts()   # parse the Scripts for Female Dialogues
    parser.parseForman()    # parse the Dialogues to locate information about man

    #parser.printStatics('Bachelor Party, The.txt', True) # this is for printing the statistics of a single script
    #parser.printStaticsFiles(parser.Scripts.files, False) # this is for printing the statistics of a bunch of scripts

    parser.writeStatistics()                             # this is for writing the statistics to the file