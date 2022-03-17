import os

#get current location folder
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

badsentencelist = []

#Generate list of badwords
with open (os.path.join(__location__, 'wrong_devs.txt')) as misFile:
    for line in misFile:

        #extract sentence out of wrong devs
        sentence_start = line.find(",")
        sentence_end = line.rfind(",")
        sentence = line[sentence_start+2:sentence_end]

        #we generate a list of bad sentences
        badsentencelist.append(sentence[:len(sentence)-1])

    
#Remove badsentences from dev.tsv
with open('dev.tsv') as devfile, open('output.tsv', 'w') as outputfile:
    for line in devfile:
        if not any(bad_sen in line for bad_sen in badsentencelist):
            outputfile.write(line)

#TODO: we now fixed the problem with wrong_devs
#TODO: we also have to fix the problems with the other part of wrong_devs sentences
#THAT IS: Using the wrong_devs index and the above loop, remove any part of the sentence predictions
#THIS should result in a prediction table and a output.tsv of equal size

#TODO using the above combine output.tsv and the two prediction sets
#TODO add the current word calculated based upon the index and sentence
