from nltk import RegexpTokenizer
from DialoguesReader import ScriptReader
from aux_class import DialogueInstance, ScriptStatics

FemaleFeatures = ['mrs', 'miss', 'ms', 'girl', 'woman', 'lady', 'tress', 'madam', 'mother', 'mom', 'mommy', 'munt', 'tess','cess']
MaleFeatures = ['mr', 'man', 'boy', 'gentleman', 'sir', 'father', 'dad', 'daddy', 'uncle']

auxFeatures = ['he', 'his', 'guy']

sentTokenizer = RegexpTokenizer(r'[A-Za-z]+')

savePath = '.\\'
saveName = 'Scripts.pkl'

def countFemaleofScene(scene, FemaleDic):

    femaleCnt, instances = set(), []
    i = 0

    while i < len(scene):
        dialogue = scene[i]
        if dialogue[0] in FemaleDic and i + 1 < len(scene):
            femaleCnt.add(dialogue[0])
               
            cnt = i + 1
            
            FemaleA = dialogue[0]
            FemaleB = scene[cnt][0]
            
            if FemaleA != FemaleB and FemaleA not in FemaleB and FemaleB not in FemaleA and scene[cnt][0] in FemaleDic:
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

    entities = sentTokenizer.tokenize(dialogue)

    for entity in entities:

        if entity[0].isupper():
            if entity.upper() in MaleDic:
                return True

        if entity.lower() in MaleFeatures or entity.lower() in auxFeatures:
            return True

    return False


class ScriptParser(object):

    def __init__(self):

        self.ScriptMap = {}
        self.savePath = savePath

        self.Scripts = ScriptReader(10)
        self.Scripts.loadScriptDic(self.savePath, saveName)

        self.files = self.Scripts.files


    def parseScripts(self):

        for filename in self.Scripts.scriptDic.keys():#self.files:

            print 'Parsing ' + filename

            script = self.Scripts.scriptDic[filename]
            Scenes, GenderDic, CharacterSet = script.Scenes, script.GenderDic, script.CharacterSet
            #print GenderDic['female']
            #print GenderDic['male']
            #print GenderDic['unknown']
            conversationInstance = DialogueInstance()



            for i, scene in enumerate(Scenes):
                if scene != []:
                    #print 'Scene, {}:'.format(i)

                    cnt, Female, instances = countFemaleofScene(scene, GenderDic['female'])
                    #print 'Female, # = ' + str(cnt), Female
                    #if len(instances) == 0:
                        #print 'No interaction between two women'
                    if len(instances) != 0:
                        for j, instance in enumerate(instances):
                            conversationInstance.Femaledialogue.append(
                                ('Scene, {}'.format(i), 'Instance, {}'.format(j), instance, Female, cnt))
                            #print 'Instance, {}:'.format(j)
                            #for dialogue in instance:
                            #    print dialogue

            self.ScriptMap[filename] = ScriptStatics(CharacterSet, GenderDic['male'],
                                                     GenderDic['female'], conversationInstance, False)

    def parseForman(self):

        for filename in self.Scripts.scriptDic.keys():
            print 'Parsing ' + filename + ' and looking for dialogues between 2 women not about man'

            conversationInstance = self.ScriptMap[filename].DialogueInstance

            for instance in conversationInstance.Femaledialogue:
                FLAG = False
                print 'Processing, ' + instance[0] + '/' + instance[1]
                for dialogue in instance[2]:
                    check = checkMaleExistence(dialogue[1], self.ScriptMap[filename].MaleSet)
                    if check:
                        conversationInstance.isAboutMan.append(True)
                        FLAG = True
                        break
                if not FLAG:
                    conversationInstance.isAboutMan.append(False)
                    self.ScriptMap[filename].canPassTest = True

        self.parseman = True

    def printStatics(self, filename, seeDialogues = False):

        if filename not in self.ScriptMap.keys():
            print 'Please input a valid filename!'
            return

        scriptStatics = self.ScriptMap[filename]
        print 'Characters: ', scriptStatics.Characters
        print 'Females, Total # of Female Characters: ', scriptStatics.numOfFemale
        print scriptStatics.FemaleSet
        print 'Males, ', scriptStatics.MaleSet

        print '# of Dialogues between women: ', scriptStatics.numOfInstance

        if self.parseman:
            print 'Could pass the test? ', scriptStatics.canPassTest

        if seeDialogues:

            conversationInstance = scriptStatics.DialogueInstance
            for i, instance in enumerate(conversationInstance.Femaledialogue):
                print instance[0] + '/' + instance[1]
                if self.parseman:
                    print 'Contains things About man? ', conversationInstance.isAboutMan[i]

                for dialogue in instance[2]:
                    print dialogue


    def printStaticsFiles(self, files, seeDialogues  = False):

        for filename in files:

            if filename not in self.ScriptMap.keys():
                print 'Invalid filename, ', filename, 'Skip.'
                continue

            print 'Processing file: ', filename
            self.printStatics(filename, seeDialogues)
            print '==========================================================================================='



if __name__ == '__main__':

    parser = ScriptParser()
    parser.parseScripts()
    parser.parseForman()

    #parser.printStatics('Drive.txt', True)
    parser.printStaticsFiles(parser.Scripts.files, False)
