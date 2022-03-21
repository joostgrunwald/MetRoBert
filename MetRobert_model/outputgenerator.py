import os

#get current location folder
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

badsentencelist = []
badindexlist = []

#Generate list of badwords
with open (os.path.join(__location__, 'wrong_devs.txt')) as misFile:
    for line in misFile:

        #extract sentence out of wrong devs
        sentence_start = line.find(",")
        sentence_end = line.rfind(",")
        sentence = line[sentence_start+2:sentence_end]

        #we generate a list of bad sentences
        badsentencelist.append(sentence[:-1])

        #we generate a list of bad indexes
        badindexlist.append(line[:sentence_start-1])

#Remove badsentences from dev.tsv
with open('dev.tsv') as devfile, open('dev2.tsv', 'w') as outputfile:
    for line in devfile:
        if str(line[0:5]) != "index" != -1:
            outputfile.write(line)
        #if all(bad_sen not in line for bad_sen in badsentencelist):
         #   outputfile.write(line)

#outputfile.close()

#Add mistakeouptuts from wrong_devs to predictions.txt
with open('predictions_dev.txt') as predsin, open('predictions_dev2.txt', 'w') as predsout:
    line_counter = 1
    previous_line = -1
    for line in predsin:

        #remove fragment part 
        pred = line.replace("dev-COV_fragment01 ","")

        #find first space
        space = pred.find(" ")

        #index of prediction
        index = pred[:space]

        if previous_line != -1 and (previous_line+1) != int(index):
            print(index)
            predsout.write(f"dev-COV_fragment01 {int(index)-1} 0" + ",-1\n")

        #only write pred if not equal to index
        if index in badindexlist:
            predsout.write(f"dev-COV_fragment01 {index} 0" + ",-1\n")

        else:
            predsout.write(line)
            line_counter = line_counter + 1


        previous_line = int(index)

with open('output.tsv', 'w') as file3:
    print("index\tsentence\tpostag\tword_index\tprediction", file=file3)
    with open('dev2.tsv', 'r') as file1:
        with open('predictions_dev2.txt', 'r') as file2:
            for line1, line2 in zip(file1, file2):
                #line1 = line.strip
                line2b = line2.strip().replace("dev-COV_fragment01","")
                komma = line2b.find(",")
                tab = line1.find("\t")
                line1 = line1.strip().replace("COV_fragment01 ","").replace("\t0\t","\t",1)

                tab = line1.find("\t")
                point = line1.find("\t",tab+2)
                sentence = line1[tab+1:point]

                ltab = line1.rfind("\t")
                word_index = line1[ltab+1:]

                senlist = sentence.split()

                word = senlist[int(word_index)]
                #! get index word index of sentence list
                #! print above as seperate column

                print(line1, "\t", word, "\t", line2.strip().replace("dev-COV_fragment01 ","")[komma:], file=file3)

#TODO: add actual word
#TODO: remove unneeded info
#prediction line = dev line + 1
#
