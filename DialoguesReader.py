# -*- coding:utf-8 -*-
from __future__ import division
import os
import codecs
from GenderGusser import gender_gusser
import pickle
from aux_class import Script_info
import random


Path = '.\Texts'
SavePath = '.\\'
saveName = 'Scripts.pkl'
MAX_FILES = 1031


# this class reads the scripts from Path

# The codes determines if a line is a Character by the following judgements:
# 1. if the whole current line is of UPPER FORM
# 2. if so, if the first following line that is not entirely formed by space(and tab), has less or equal space(and tab)
# 3. if so, then the current line is a Character,
# 4. if not, then it's not a Character


class ScriptReader(object):

    def __init__(self, num_scripts):
        '''
        :param num_scripts: specify how many scripts you want to process, if number you enter is larger than MAX_FILES,
                            then means you want to process all the files
                            NOTE: process all the files is extremely time consuming, I would recommend to use the pre-processed
                                file Scripts.pkl for further test
                            And the test for this part, you could just enter 5 or 10 for num_scripts to see how it works
        '''

        self.scriptDic = {}         # stores each script
        self.Path = Path            # script path
        self.files = os.listdir(self.Path)  # all names of the scripts in Path

        if num_scripts < MAX_FILES:     #
            random.shuffle(self.files)
            self.files = self.files[:num_scripts]

    def Initializer(self):

        # this function is used to read scripts and process the Scenes and Characters and Genders

        for j in range(len(self.files)):
            filename = self.files[j]
            with codecs.open(os.path.join(Path, filename), 'r', encoding = 'utf-8') as f:

                print 'Processing ' + filename

                lines = f.readlines()
                i = 0
                Scenes = [] # Stores the scenes in which there are conversations among Characters
                tmp = []    # tmp list to store conversations in one scene

                GenderDic = {'female': set(), 'male': set(), 'unknown': set()} # GenderDic
                CharacterSet = set() # Store all characters

                while i < len(lines):
                    line = lines[i]
                    if line.strip() != '' and line.strip().isupper(): # This function is used to determine if it is a Character
                        #print line.strip()

                        count = len(line) - len(line.strip(' ').strip('\t'))
                        cnt = i + 1

                        while cnt < len(lines) and lines[cnt].strip() == '': # Find the first lines following the potential Character that is not fully space(and tab)
                            cnt += 1

                        if cnt == len(lines): break

                        supposeCount = len(lines[cnt]) - len(lines[cnt].strip(' ').strip('\t'))

                        if lines[cnt].isupper() or (count <= supposeCount and '(' not in lines[cnt]): # then it's not a Character, which also means
                            Scenes.append(tmp)                                                        # it's the end of the current scene
                            tmp = []
                            i = cnt
                            continue
                        #print count, supposeCount, line, lines[cnt]

                        # if the codes runs here, then we found a Character.
                        # we need to identify it's gender first

                        entity = line.strip().encode('utf-8')
                        if entity not in CharacterSet:
                            CharacterSet.add(entity)
                            gender = gender_gusser(entity)
                            GenderDic[gender].add(entity)

                        if entity not in GenderDic['unknown']:
                            dialogue = ""

                            # then record the actor's lines of the current Character

                            while cnt < len(lines) and lines[cnt].strip() != "":
                                dialogue += lines[cnt].strip() + ' '
                                cnt += 1

                            # put it into tmp anf further will be in the Scenes
                            tmp.append((line.strip().encode('utf-8'), dialogue.encode('utf-8')))
                            i = cnt -1

                    i += 1

            self.scriptDic[filename] = Script_info(Scenes, GenderDic, CharacterSet)


    # Normal pickle save/load functions

    def saveScriptDic(self, path, filename):
        with open(os.path.join(path, filename), 'w') as f:
            pickle.dump((self.scriptDic, self.files), f)

    def loadScriptDic(self, path, filename):
        with open(os.path.join(path, filename), 'r') as f:
            self.scriptDic, self.files = pickle.load(f)


if __name__ == '__main__':

    reader = ScriptReader(256)  # change the 10 to your desired number which denotes the number of scripts to be processed
    reader.Initializer()        # process the scripts
    reader.saveScriptDic(SavePath, saveName)  # save the processed Scenes, GenderDics and CharacterSets,
                                                # please change the saveName to a different name such that
                                                # the content original pickle won't be replaced
