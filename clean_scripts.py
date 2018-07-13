import os
import codecs
from collections import Counter

savePath = '.\Texts'

noisePath = '.\NoiseTexts'

def clean_scripts():

    files = os.listdir(savePath)
    #files = ['Escape From New York.txt']

    for filename in files:
        count = []
        with codecs.open(os.path.join(savePath,filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()

            i = 0
            while i < len(lines):
                line = lines[i]

                if line.strip() != "":
                    count.append(len(line) - len(line.strip(' ').strip('\t')))

                i += 1

        count = Counter(count).most_common(3)
        if len(count) < 3 or len(count) == 1 or count[0][1] / count[1][1] > 100:
            #print filename, count
            os.rename(os.path.join(savePath, filename), os.path.join(noisePath, filename))
            print filename, count[0]
