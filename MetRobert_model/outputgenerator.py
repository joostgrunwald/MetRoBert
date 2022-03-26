import os

def main(location="empty", pos_tags=[]):

    if (location == "empty"):
        #get current location folder
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

    #In else case location is user specified
    #TODO: maybe check if file is present and/or catch file not found error?

    badsentencelist = []
    badindexlist = []

    #Generate list of badwords
    with open (os.path.join(location, 'wrong_devs.txt')) as misFile:
        for line in misFile:

            #extract sentence out of wrong devs
            sentence_start = line.find(",")
            sentence_end = line.rfind(",")
            sentence = line[sentence_start+2:sentence_end]

            #we generate a list of bad sentences
            badsentencelist.append(sentence[:-1])

            #we generate a list of bad indexes
            badindexlist.append(line[:sentence_start-1])

    #Remove first rule from dev.tsv
    with open(os.path.join(location, 'dev.tsv')) as devfile, open(os.path.join(location, 'dev2.tsv'), 'w') as outputfile:
        for line in devfile:
            if str(line[:5]) != "index":
                outputfile.write(line)
                #if all(bad_sen not in line for bad_sen in badsentencelist):
                #   outputfile.write(line)

    #outputfile.close()
    missing_lines = 0
    bad_indexes = 0

    #Add mistakeouptuts from wrong_devs to predictions.txt
    with open(os.path.join(location, 'predictions_dev.txt')) as predsin, open(os.path.join(location, 'predictions_dev2.txt'), 'w') as predsout:
        line_counter = 1
        previous_line = -1
        preprevious_line = -1

        for line in predsin:

            #remove fragment part 
            pred = line.replace("dev-COV_fragment01 ","")

            #find first space
            space = pred.find(" ")

            #index of prediction
            index = pred[:space]

            if previous_line != -1 and (previous_line+1) != int(index):
                #print(index)
                missing_lines = missing_lines + 1
                predsout.write(f"dev-COV_fragment01 {int(index)-1} 0" + ",-1\n")

                #missing line

            #only write pred if not equal to index
            if index in badindexlist:
                bad_indexes = bad_indexes + 1
                predsout.write(f"dev-COV_fragment01 {index} 0" + ",-1\n")

            else:
                predsout.write(line)
                line_counter = line_counter + 1

            preprevious_line = previous_line
            previous_line = int(index)

    error_amount = 0
    minone_amount = 0
    out_of_bounds = 0

    with open(os.path.join(location, 'output.tsv'), 'w') as file3:
        print("index\tsentence\tpostag\tword_index\tword\tprediction", file=file3)
        with open(os.path.join(location, 'dev2.tsv'), 'r') as file1:
            with open(os.path.join(location, 'predictions_dev2.txt'), 'r') as file2:
                for line1, line2 in zip(file1, file2):

                    #cleanup
                    line2b = line2.strip().replace("dev-COV_fragment01","")
                    komma = line2b.find(",")
                    tab = line1.find("\t")
                    line1 = line1.strip().replace("COV_fragment01 ","").replace("\t0\t","\t",1)

                    #retrieve sentence
                    tab = line1.find("\t")
                    point = line1.find("\t",tab+2)
                    sentence = line1[tab+1:point]

                    #retrieve word index
                    ltab = line1.rfind("\t")
                    word_index = line1[ltab+1:]

                    #retrieve pos tag
                    ltab2 = line1.rfind("\t",0,ltab)
                    pos_tag = line1[ltab2+1:ltab]


                    #! FILTER OUT UNWANTED POS TAGS
                    toskip = False
                    for pos in pos_tags:
                        if pos_tag.lower().find(pos) != -1:
                            toskip = True
                    if toskip == True:
                        continue

                    senlist = sentence.split()

                    word = "ERROR"
                    if "-1" in str(line2):
                        minone_amount = minone_amount + 1

                    elif int(word_index) <= len(senlist):
                        word = senlist[int(word_index)]
                    else: 
                        out_of_bounds = out_of_bounds + 1
                    #? ERROR CAUSED BY MISSING PREDICTION (NO -1 PRESENT)
                    if word == "ERROR":
                        error_amount = error_amount + 1

                    print(line1, "\t", word, "\t", line2.strip().replace("dev-COV_fragment01 ","")[komma:], file=file3)


    #? DIAGNOSTICS
    print("BADINDEXLIST")
    print(f"wrong dev bad indexes: {len(badindexlist)} times")
    print("")
    print("PREDS")
    print(f"missing_lines: {missing_lines} times")
    print(f"bad_index: {bad_indexes} times")
    print("")
    print("OUTPUT.TSV")
    print(f"out of bounds: {out_of_bounds} times")
    print(f"-1 supplied: {minone_amount} times")
    print(f"word error: {error_amount} times")

    if(error_amount != out_of_bounds + minone_amount):
        print("ERROR: out of bounds cases + -1 cases do not equal amount of errors")

    if (missing_lines + bad_indexes != minone_amount):
        print("ERROR: output of preds cleaning does not match input of output.tsv generation")

if __name__ == "__main__":
    main()
