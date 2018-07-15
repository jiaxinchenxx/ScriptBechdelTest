from __future__ import division
from gender_detector import GenderDetector
from nltk import RegexpTokenizer


detectorus = GenderDetector('us') # It can also be ar, uk, uy.
detectorar = GenderDetector('ar')
detectoruk = GenderDetector('uk')
detectoruy = GenderDetector('uy')
detector = [detectorus, detectoruk, detectoruy, detectorar]

FemaleFeatures = ['mrs', 'miss', 'ms', 'girl', 'woman', 'lady', 'madam', 'mother', 'mom', 'mommy', 'munt']
FemaleSuffix = ['tress', 'tess', 'cess']
MaleFeatures = ['mr', 'man', 'boy', 'gentleman', 'sir', 'father', 'dad', 'daddy', 'uncle']

tokenizer = RegexpTokenizer(r'[A-Z]+')


# this methods is very expensive, and it's the bottleneck of the code.
# most of the time will be consumed in determining whether the character is Male or Female
# the library here is a opensource library called gender_detector,
# the installation instruction could be seen in README.txt


def gender_gusser(entity, withFeature = False):
    '''

    :param entity: The name enitity found in the scripts
    :param withFeature: if True, then Character like LITTLE GIRL, OLD WOMEN will be counted as a Female Character
                        if False, only Female name like Helen, Hannah will be counted as a Female Character
    :return: gender of entity
    '''

    entity = tokenizer.tokenize(entity)

    if withFeature:
        for ff in FemaleFeatures:
            if ff.upper() in entity:
                return 'female'

        for mf in MaleFeatures:
            if mf.upper() in entity:
                return 'male'

    for name in entity:
        if name == 'THE' or name == 'YOUNG' or name == 'OLD':
            continue

        for detec in detector:
            gender = detec.guess(name)
            if gender != 'unknown':
                return gender

        if withFeature:
            for fs in FemaleSuffix:
                if name.lower().endswith(fs):
                    return 'female'

    return 'unknown'