# ScriptBechdelTest
Here is instructions about running the code.

Python -> 2.7.14
Required lib:
gender_detector -> pip install gender_detector 
nltk            -> pip install nltk


The pipeline of the code:
1. run Scrapy_Scripts to scrape scripts from imsdb.
2. run clean_scripts to clear noise scripts
3. run DialoguesReader to process the scripts for their Scenes, GenderDics and CharacterSets
4. run BechdelTest to get the Statistics information.


However, it is highly recommended that you use the pre-downloaded and pre-cleaned scripts file and pre-processed pickle files to test the later functions.
The pre-downloaded scripts could just avoid you from scraping the scripts from IMSDB and clearing the noise files again which is time consuming.
(Which means if you use that, you could just skip the step 1 and 2)

The pre-processed pickle files contain 256 scripts with their Scenes, GenderDics and CharacterSets repectively.
You could certainly run DialoguesReader again and enter the scripts you want to process(num_scripts) and get the pickle files yourself,
But it would be very time consuming cause that judgement of the genders of given Characters will be a huge bottleneck.
  

Such that, for the file DialoguesReader.py, which is used to read the scripts and get Scenes, GenderDic and CharacterSet of scripts.
You could change:

reader = ScriptReader(10) --> reader = ScriptReader(num_scripts you want) to read Scenes, GenderDics and CharacterSets of your desired number of scripts.
if you do that, please change the variable saveName in that file such that you won't change the content of pre-processed pickle file.

If you just want to give the function a brief glance, please leave the num_scripts of criptReader() with 5 or 10, such that you only need to process 5 or 10 files and it won't take much time. Also remember to change the variable saveName in that file.



After that, you may get the Scripts.pkl and maybe your another pickle file contains 5 or 10 scripts which is the output of your test of the DialogueReader.

Then you could test the BechdelTest.py.

The instruction is in the comment of the code, the pre-set saveName is the pre-processed information that is mentioned before.
You could set the parameter as your own savename which you generate on your own when you test the DialoguesReader.py
