import os
import codecs
from collections import Counter

savePath = '.\Texts'
noisePath = '.\NoiseTexts'


# This methods, will clean up the noise scripts in files with naive method
# Cause the code determines if a line is a Character by the following judgements:
# 1. if the whole current line is of UPPER FORM
# 2. if so, if the first following line that is not entirely formed by space(and tab), has less or equal space(and tab)
# 3. if so, then the current line is a Character,
# 4. if not, then it's not a Character

# Such that this method clears the scripts with following feature:
# All lines or most of the lines in it has the same number of space(and tab)

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
        if len(count) < 3 or len(count) == 1 or count[0][1] / count[1][1] > 100:  # this number 100, is set subjectively
            #print filename, count
            os.rename(os.path.join(savePath, filename), os.path.join(noisePath, filename))
            print filename, count[0]


clean_scripts()