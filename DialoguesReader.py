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
MAX_FILES = 1087

'''
files = os.listdir('.\Texts2')
CUTTO = 0
DISSOLVETO = 0
TOTAL = len(files)
for file in files:

    with codecs.open(os.path.join(Path, file), 'r', encoding = 'utf-8') as f:
        lines = f.readlines()

    Flag = False
    for line in lines:
        if 'CUT TO:' in line:
            CUTTO += 1
            Flag = True
            break
        if 'DISSOLVE TO' in line:
            DISSOLVETO += 1
            Flag = True
            break
    if not Flag:
        print file

print TOTAL, CUTTO, DISSOLVETO

'''
"""
class Script_info(object):

    def __init__(self, Scenes, GenderDic, CharacterDic):
        self.Scenes = Scenes
        self.GenderDic = GenderDic
        self.CharacterDic = CharacterDic
"""

class ScriptReader(object):

    def __init__(self, num_scripts):
        self.scriptDic = {}
        self.Path = Path
        self.files = os.listdir(self.Path)

        if num_scripts < MAX_FILES:
            random.shuffle(self.files)
            self.files = self.files[:num_scripts]

    def Initializer(self):


        for j in range(len(self.files)):
            filename = self.files[j]
            with codecs.open(os.path.join(Path, filename), 'r', encoding = 'utf-8') as f:

                print 'Processing ' + filename

                lines = f.readlines()
                i = 0
                Scenes = []
                tmp = []

                GenderDic = {'female': set(), 'male': set(), 'unknown': set()}
                CharacterSet = set()

                while i < len(lines):
                    line = lines[i]
                    if line.strip() != '' and line.strip().isupper():
                        #print line.strip()

                        count = len(line) - len(line.strip(' ').strip('\t'))
                        cnt = i + 1
                        if cnt == len(lines): break

                        while cnt < len(lines) and lines[cnt].strip() == '': # 20180713
                            cnt += 1

                        supposeCount = len(lines[cnt]) - len(lines[cnt].strip(' ').strip('\t'))

                        if lines[cnt].isupper() or (count <= supposeCount and '(' not in lines[cnt]):  # lines[cnt].strip() == "" or (
                            Scenes.append(tmp)
                            tmp = []
                            i = cnt
                            continue
                        #print count, supposeCount, line, lines[cnt]

                        entity = line.strip().encode('utf-8')
                        if entity not in CharacterSet:
                            CharacterSet.add(entity)
                            gender = gender_gusser(entity)
                            GenderDic[gender].add(entity)

                        if entity not in GenderDic['unknown']:
                            dialogue = ""


                            while lines[cnt].strip() != "" and cnt < len(lines):
                                dialogue += lines[cnt].strip() + ' '
                                cnt += 1
                            tmp.append((line.strip().encode('utf-8'), dialogue.encode('utf-8')))
                            i = cnt -1

                    i += 1

            self.scriptDic[filename] = Script_info(Scenes, GenderDic, CharacterSet)


    def saveScriptDic(self, path, filename):
        with open(os.path.join(path, filename), 'w') as f:
            pickle.dump((self.scriptDic, self.files), f)

    def loadScriptDic(self, path, filename):
        with open(os.path.join(path, filename), 'r') as f:
            self.scriptDic, self.files = pickle.load(f)


if __name__ == '__main__':

    reader = ScriptReader(10)
    reader.Initializer()
    reader.saveScriptDic(SavePath, saveName)


'''
reader = ScriptReader()
reader.Initializer()
#print len(reader.scriptDic)
for key in reader.scriptDic['Avengers, The (2012).txt'].GenderDic.keys():
    print key
    print reader.scriptDic['Avengers, The (2012).txt'].GenderDic[key]
'''
"""
for i, scene in enumerate(Scenes):
    if scene != []:
        print 'Scene, {}:'.format(i)
        for dialogue in scene:
            print dialogue
"""
