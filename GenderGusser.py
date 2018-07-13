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

def gender_gusser_without_feature(entity):


    entity = tokenizer.tokenize(entity)

#    for ff in FemaleFeatures:
#        if ff.upper() in entity:
#            return 'female'
#    for mf in MaleFeatures:
#        if mf.upper() in entity:
#            return 'male'


    for name in entity:
        if name == 'THE' or name == 'YOUNG' or name == 'OLD':
            continue
        #print name
        for detec in detector:
            gender = detec.guess(name)
            if gender != 'unknown':
                return gender

#        for fs in FemaleSuffix:
#            if len(fs) < len(name) and fs.lower() == name[len(name) - len(fs):].lower():
#                return 'female'


    return 'unknown'

def gender_gusser(entity, withFeature = False):

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
                if len(fs) < len(name) and fs.lower() == name[len(name) - len(fs):].lower():
                    return 'female'



    return 'unknown'
