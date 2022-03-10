##############
# dependencies#
##############
from lxml import etree
from io import BytesIO
import xml.etree.ElementTree as ET
import os
import codecs

################
# USER INTERFACE#
################
print(
    " _______                                                                                                         "
)
print(
    "|       \                                                                                                        "
)
print(
    "| $$$$$$$\ ______    _______  ______ ____    ______    ______    ______    ______    _______   ______    ______  "
)
print(
    "| $$__/ $$|      \  /       \|      \    \  |      \  /      \  |      \  /      \  /       \ /      \  /      \ "
)
print(
    "| $$    $$ \$$$$$$\|  $$$$$$$| $$$$$$\$$$$\  \$$$$$$\|  $$$$$$\  \$$$$$$\|  $$$$$$\|  $$$$$$$|  $$$$$$\|  $$$$$$\\"
)
print(
    "| $$$$$$$ /      $$ \$$    \ | $$ | $$ | $$ /      $$| $$  | $$ /      $$| $$   \$$ \$$    \ | $$    $$| $$   \$$"
)
print(
    "| $$     |  $$$$$$$ _\$$$$$$\| $$ | $$ | $$|  $$$$$$$| $$__/ $$|  $$$$$$$| $$       _\$$$$$$\| $$$$$$$$| $$      "
)
print(
    "| $$      \$$    $$|       $$| $$ | $$ | $$ \$$    $$| $$    $$ \$$    $$| $$      |       $$ \$$     \| $$      "
)
print(
    " \$$       \$$$$$$$ \$$$$$$$  \$$  \$$  \$$  \$$$$$$$| $$$$$$$   \$$$$$$$ \$$       \$$$$$$$   \$$$$$$$ \$$      "
)
print(
    "                                                     | $$                                                        "
)
print(
    "                                                     | $$                                                        "
)
print(
    "                                                      \$$                                                        "
)
print("")
print("This program was written by Joost Grunwald for the Radboud university.")
print(
    "The program parses the data of the dutch pasma corpus to make it usable for a context based neural network."
)
print("")

##################
# GLOBAL VARIABLES#
##################
filenumber = 0  # will later on be incremented for new file
file_fragment = 0
sent_no = 0

#adjust for partitioning
train_test_border = 29623 #default 35500

directory = r"C:\Users\Josso\Documents\Radboud\corpus_original\gesprekken"
subdirectories = os.listdir(directory)

for directory_d2_first in subdirectories:
    # print(directory_d2_first)
    directory_d2 = directory + "\\" + directory_d2_first
    # for filename in os.listdir(directory_d2):
    # if filename.endswith(".xml"):
    # print(filename)

#! WE LIST ALL OUTPUTDIRECTORIES USED
outputdirectory_train = (
    r"C:\Users\Josso\Documents\Radboud\conv_output\train.tsv"
)
outputdirectory_test = (
    r"C:\Users\Josso\Documents\Radboud\conv_output\test.tsv"
)
outputdirectory_dev = (
    r"C:\Users\Josso\Documents\Radboud\conv_output\dev.tsv"
)

# ? WE ADD ALL DIRECTORY HEADERS
f = codecs.open(outputdirectory_train, "w", encoding="utf8")
f.write("index  label   sentence    POS w_index" + "\n")

g = codecs.open(outputdirectory_test, "w", encoding="utf8")
g.write("index  label   sentence    POS w_index" + "\n")

h = codecs.open(outputdirectory_dev, "w", encoding="utf8")
h.write("index  label   sentence    POS w_index" + "\n")


for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        adder = 0
        print(filename)
        filenumber = filenumber + 1
        file_fragment = file_fragment + 1
        filedirectory = directory + "\\" + filename
        genre = "news"
        parser = etree.XMLParser(ns_clean=True, remove_comments=True)
        tree = etree.parse(filedirectory, parser)
        root = tree.getroot()

        # <ptext ref="Aec2.txt">
        for filename_scrape in root.iter("ptext"):
            # only one occurence, not really a for loop, stores filename
            filename = filename_scrape.get("ref")

        filename = filename.replace(".txt", "")  # remove extension

        ############################################
        # PART 1: get Sentence, fulltext and context#
        ############################################
        fulltext = ""
        sentencelist = []
        contextlist = []
        for sent in root.iter("sent"):
            for child in sent:
                sentence = ""
                wordtext = ""
                for child_of_child in child:
                    if child_of_child.get("s") == "UNKNOWN":
                        for child_3 in child_of_child:
                            temporary = ""
                            for child_4 in child_3:
                                if not str(child_4.text) == "None":
                                    wordtext = wordtext + child_4.text
                                    temporary = child_4.text
                            if (temporary == "") and not str(child_3.text) == "None":
                                wordtext = wordtext + child_3.text
                                temporary = child_3.text

                            wordtext = wordtext + " "
                            sentence = wordtext
                    else:
                        temporary = ""
                        for child3 in child_of_child:
                            if not str(child3.text) == "None":
                                wordtext = wordtext + child3.text
                                temporary = child3.text
                        if temporary == "":
                            if not str(child_of_child.text) == "None":
                                wordtext = wordtext + child_of_child.text
                                temporary = child_of_child.text
                        wordtext = wordtext + " "
                        sentence = wordtext

                    # we need to make some adjustments to make the sentence be more correct again.
                if sentence != "" and sentence != "\n":
                    sentence = sentence.replace(" , ", ", ")
                    sentence = sentence.replace(" ; ", "; ")
                    sentence = sentence.replace(" .", ".")
                    sentence = sentence.replace(" : ", ": ")
                    sentence = sentence.replace(" ( ", " (")
                    sentence = sentence.replace(" ) ", ") ")
                    sentence = sentence.replace(" )", ")")
                    sentence = sentence.replace(" ',", "',")
                    if sentence[0:2] == "' ":
                        sentence = "'" + sentence[2:]
                    sentence = sentence.replace(" ' ", " '", 1)
                    sentence = sentence.replace(" ' ", "' ", 1)
                    sentence = sentence.replace(" ' ", " '", 1)
                    sentence = sentence.replace(" ' ", "' ", 1)
                    sentence = sentence.replace(" ' ", " '", 1)
                    sentence = sentence.replace(" ' ", "' ", 1)
                    
                    if sentence.find("'") != -1:
                        quote = sentence.find("'")
                        quoter = sentence.find("'")
                        #if len(sentence) >= quote + 1 and sentence[quote+1] == " ":
                         #   i = 1
                            #sentence = sentence[0:quote] + "'" + sentence[quote+2:]
                   
                    #Todo count occurences of '
                    # do count divided by 2
                    # make copy sentence
                    # loop over counts
                    # fix set of quotation marks for each count
                    sentencelist.append(sentence)

        sentences_amount = len(sentencelist) - 1
        counter = 0
        previous_sen = ""
        secondsentences = sentencelist

        # we format the sentence adding points when needed, to make it even more readable and hopefully get better results in our neural network (upgrade recall value)
        for sentence in sentencelist:
            #print(sentence)
            counter = counter + 1
            if counter == 2 or counter == 3 or counter == 4:
                continue
            elif counter == 5:
                # reset
                counter = 0
                continue
            elif counter == 1:
                con_sentence = ""
                index = sentencelist.index(sentence)
                context = ""
                # added begin
                if index <= sentences_amount:
                    con_sentence = sentencelist[index]
                    if con_sentence[len(con_sentence) - 1 :] == " ":
                        con_sentence = con_sentence[: len(con_sentence) - 1]
                        if con_sentence[len(con_sentence) - 1 :].isalpha():
                            con_sentence = con_sentence + "."
                    elif con_sentence[len(con_sentence) - 1 :].isalpha():
                        con_sentence = con_sentence + "."
                    context = context + con_sentence
                # added end
                if index + 1 <= sentences_amount:
                    con_sentence = sentencelist[index + 1]
                    if con_sentence[len(con_sentence) - 1 :] == " ":
                        con_sentence = con_sentence[: len(con_sentence) - 1]
                        if con_sentence[len(con_sentence) - 1 :].isalpha():
                            con_sentence = con_sentence + "."
                    elif con_sentence[len(con_sentence) - 1 :].isalpha():
                        con_sentence = con_sentence + "."
                    context = context + con_sentence
                if index + 2 <= sentences_amount:
                    con_sentence = sentencelist[index + 2]
                    if con_sentence[len(con_sentence) - 1 :] == " ":
                        con_sentence = con_sentence[: len(con_sentence) - 1]
                        if con_sentence[len(con_sentence) - 1 :].isalpha():
                            con_sentence = con_sentence + "."
                    elif con_sentence[len(con_sentence) - 1 :].isalpha():
                        con_sentence = con_sentence + "."
                    context = context + con_sentence
                if index + 3 <= sentences_amount:
                    con_sentence = sentencelist[index + 3]
                    if con_sentence[len(con_sentence) - 1 :] == " ":
                        con_sentence = con_sentence[: len(con_sentence) - 1]
                        if con_sentence[len(con_sentence) - 1 :].isalpha():
                            con_sentence = con_sentence + "."
                    elif con_sentence[len(con_sentence) - 1 :].isalpha():
                        con_sentence = con_sentence + "."
                    context = context + con_sentence
                if index + 4 <= sentences_amount:
                    con_sentence = sentencelist[index + 4]
                    if con_sentence[len(con_sentence) - 1 :] == " ":
                        con_sentence = con_sentence[: len(con_sentence) - 1]
                        if con_sentence[len(con_sentence) - 1 :].isalpha():
                            con_sentence = con_sentence + "."
                    elif con_sentence[len(con_sentence) - 1 :].isalpha():
                        con_sentence = con_sentence + "."
                    context = context + con_sentence

                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)

        for i in range(len(secondsentences)):
            sentence = sentencelist[i]

            # clean the actual sentence
            if sentence[len(sentence) - 1 :] == " ":
                sentence = sentence[: len(sentence) - 1]
                if sentence[len(sentence) - 1 :].isalpha() or sentence[len(sentence) - 1 :].isnumeric():
                    sentence = sentence + "."
            elif sentence[len(sentence) - 1 :].isalpha() or sentence[len(sentence) - 1 :].isnumeric():
                sentence = sentence + "."

            secondsentences[i] = sentence

        # for context in contextlist:
        # print(context)

        ################################################
        # PART 2: get verb, verb lemma and bool metaphor#
        ################################################
        # print(".cvs syntax output:")
        output = ""
        for sent in root.iter("sent"):
            for child in sent:
                letsofar = 0
                for child_of_child in child:
                    metaphor = 0
                    verbtext = ""
                    verb_lemma = ""
                        
                    if child_of_child.get("s") == "UNKNOWN":
                        letsofar = 0
                        for child3 in child_of_child:
                            # replaced this with an always true comment
                            if True == True:

                                pos_tag = ""

                                if "LET()" in child3.get("pos"):
                                    letsofar = letsofar + 1                                

                                # ? GATHER POS TAG FROM pos
                                if "WW(" in child3.get("pos"):
                                    pos_tag = "VERB"
                                elif "N(" in child3.get("pos"):
                                    pos_tag = "NOUN"

                                # ? Het correct taggen van werkwoorden, zelfstandige en bijvoeglijke naamwoorden.
                                if "WW(" in child3.get("pos"):
                                    pos_tag = "VERB"
                                elif "N(" in child3.get("pos"):
                                    pos_tag = "NOUN"
                                elif "ADJ(" in child3.get("pos"):
                                    pos_tag = "ADJ"

                                # ? Het correct taggen van voornaamwoorden
                                elif "VNW(" in child3.get(
                                    "pos"
                                ) and "adv-pron" in child3.get("pos"):
                                    pos_tag = "ADV"
                                elif "VNW(" in child3.get(
                                    "pos"
                                ) and "prenom" in child3.get("pos"):
                                    pos_tag = "DET"
                                elif (
                                    "VNW(" in child3.get("pos")
                                    and "pron" in child3.get("pos")
                                    and str(child3.get("word")).lower() is not "het"
                                ):
                                    pos_tag = "PRON"

                                # ? Het correct taggen van bijwoorden, lidwoorden en nummers
                                elif "BW(" in child3.get("pos"):
                                    pos_tag = "ADV"
                                elif "LID(" in child3.get("pos"):
                                    pos_tag = "DET"
                                elif child3.get("lem").isnumeric():
                                    pos_tag = "NUM"
                                # TODO ADD OTHER KINDS OF POS TAGS

                                # gather verb lemma
                                verb_lemma = child3.get("lem")

                                # gather verb
                                for child4 in child3:
                                    verbtext = child4.text
                                    metaphor = 1
                                if verbtext == "":
                                    verbtext = child3.text
                                    metaphor = 0

                                # gather sentence number
                                sent_number = sent.get("id")

                                # gather corresponding sentence
                                if pos_tag is not "":
                                    index_sen = int(sent_number) + adder
                                    cor_sentence = sentencelist[index_sen]
                                    if cor_sentence.find(verbtext) == -1:
                                        adder = adder + 1
                                        index_sen = int(sent_number) + adder
                                        cor_sentence = sentencelist[index_sen]
                                        if cor_sentence.find(verbtext) == -1:
                                            adder = adder - 2
                                            index_sen = int(sent_number) + adder
                                            cor_sentence = sentencelist[index_sen]
                                            if cor_sentence.find(verbtext) == -1:
                                                adder = adder + 3
                                                index_sen = int(sent_number) + adder
                                                cor_sentence = sentencelist[index_sen]
                                                if cor_sentence.find(verbtext) == -1:
                                                    adder = adder - 4
                                                    index_sen = int(sent_number) + adder
                                                    cor_sentence = sentencelist[
                                                        index_sen
                                                    ]
                                                    if (
                                                        cor_sentence.find(verbtext)
                                                        == -1
                                                    ):
                                                        adder = adder + 4
                                                        index_sen = (
                                                            int(sent_number) + adder
                                                        )
                                                        cor_sentence = sentencelist[
                                                            index_sen
                                                        ]

                                    # gather corresponding context
                                    cor_context = contextlist[index_sen]

                                    # gather text_segment_id
                                    text_segment = filename + "-fragment01"

                                    # gather word offset
                                    word_offset = child3.get("ref")
                                    last_index = word_offset.rfind(".")
                                    word_offset = word_offset[last_index + 1 :]
                                    word_offset = word_offset.replace(".", "")

                                    # gather sentence start id
                                    sen_start_index = cor_context.find(cor_sentence)

                                    # gather sentence end id
                                    if index_sen + 1 <= len(sentencelist):
                                        next_sentence = sentencelist[index_sen + 1]
                                        sen_end_index = (
                                            cor_context.find(next_sentence) - 1
                                        )
                                        if (
                                            sen_end_index == -2
                                        ):  # not found so last sentence of context
                                            sen_end_index = len(cor_context)
                                    else:
                                        sen_end_index = len(cor_context)

                                    # sentence offset
                                    sen_offset = sent_number

                                    if (
                                        cor_sentence.find(",") != -1
                                        or cor_sentence.find(";") != -1
                                    ):
                                        cor_sentence = '"' + cor_sentence + '"'

                                    if cor_context.find("  ") != -1:
                                        cor_context = cor_context.replace("  ", " ")

                                    if cor_sentence[0:1] == " ":
                                        cor_sentence = cor_sentence[1:]

                                    if cor_sentence[0:1] == " ":
                                        cor_sentence = cor_sentence[1:]

                                    # divide into test and train
                                    # 70 percent train, 30 percent test
                                    # 5757 training data
                                    # 2467 test data
                                    if pos_tag is not "":
                                        sent_no = sent_no + 1

                                        output = (
                                            text_segment
                                            + " "
                                            + str(sent_no)
                                            + "\t"
                                            + str(metaphor)
                                            + "\t"
                                            + cor_sentence
                                            + "\t"
                                            + str(pos_tag)
                                            + "\t"
                                            + str(int(word_offset)-1-letsofar)
                                        )

                                        if sent_no <= train_test_border:  # was 33000
                                            f.write(output + "\n")
                                        elif sent_no > train_test_border:
                                            g.write(output + "\n")

                    elif str(child_of_child.get("pos")) != "None":

                        pos_tag = ""

                        if "LET()" in child_of_child.get("pos"):
                            letsofar = letsofar + 1  

                        # ? Het correct taggen van werkwoorden, zelfstandige en bijvoeglijke naamwoorden.
                        if "WW(" in child_of_child.get("pos"):
                            pos_tag = "VERB"
                        elif "N(" in child_of_child.get("pos"):
                            pos_tag = "NOUN"
                        elif "ADJ(" in child_of_child.get("pos"):
                            pos_tag = "ADJ"

                        # ? Het correct taggen van voornaamwoorden
                        elif "VNW(" in child_of_child.get(
                            "pos"
                        ) and "adv-pron" in child_of_child.get("pos"):
                            pos_tag = "ADV"
                        elif "VNW(" in child_of_child.get(
                            "pos"
                        ) and "prenom" in child_of_child.get("pos"):
                            pos_tag = "DET"
                        elif (
                            "VNW(" in child_of_child.get("pos")
                            and "pron" in child_of_child.get("pos")
                            and str(child_of_child.get("word")).lower() is not "het"
                        ):
                            pos_tag = "PRON"

                        # ? Het correct taggen van bijwoorden, lidwoorden en nummers
                        elif "BW(" in child_of_child.get("pos"):
                            pos_tag = "ADV"
                        elif "LID(" in child_of_child.get("pos"):
                            pos_tag = "DET"
                        elif child_of_child.get("lem").isnumeric():
                            pos_tag = "NUM"
                        # TODO ADD OTHER KINDS OF POS TAGS

                        # gather verb lemma
                        verb_lemma = child_of_child.get("lem")

                        # gather verb
                        for child3 in child_of_child:
                            verbtext = child3.text
                            metaphor = 1
                        if verbtext == "":
                            verbtext = child_of_child.text
                            metaphor = 0

                        # gather sentence number
                        sent_number = sent.get("id")


                        condition = True
                        # gather corresponding sentence
                        if pos_tag is not "":
                            index_sen = int(sent_number) + adder
                            cor_sentence = sentencelist[index_sen]
                            if cor_sentence.find(str(verbtext)) == -1:
                                adder = adder + 1
                                index_sen = int(sent_number) + adder
                                if (index_sen < len(sentencelist)):
                                    cor_sentence = sentencelist[index_sen]
                                    if (cor_sentence.find(str(verbtext)) == -1):
                                        condition = False
                                else:
                                    condition = False
                                    
                                if condition == False:
                                    adder = adder - 2
                                    index_sen = int(sent_number) + adder
                                    cor_sentence = sentencelist[index_sen]
                                    if cor_sentence.find(str(verbtext)) == -1:
                                        adder = adder + 3
                                        index_sen = int(sent_number) + adder
                                        cor_sentence = sentencelist[index_sen]
                                        if cor_sentence.find(str(verbtext)) == -1:
                                            adder = adder - 4
                                            index_sen = int(sent_number) + adder
                                            cor_sentence = sentencelist[index_sen]
                                            if cor_sentence.find(str(verbtext)) == -1:
                                                adder = adder + 4
                                                index_sen = int(sent_number) + adder
                                                cor_sentence = sentencelist[index_sen]
                                                if cor_sentence.find(str(verbtext)) == -1:
                                                    adder = adder -5
                                                    index_sen = int(sent_number) + adder
                                                    cor_sentence = sentencelist[index_sen]
                                                    if cor_sentence.find(str(verbtext)) == -1:
                                                        adder = adder + 5
                                                        index_sen = int(sent_number) + adder
                                                        cor_sentence = sentencelist[index_sen]
                                                        if cor_sentence.find(str(verbtext)) == -1:
                                                            adder = adder - 6
                                                            index_sen = int(sent_number) + adder
                                                            cor_sentence = sentencelist[index_sen]
                                                            if cor_sentence.find(str(verbtext)) == -1:
                                                                adder = adder + 6
                                                                index_sen = int(sent_number) + adder
                                                                cor_sentence = sentencelist[index_sen]
                                                                if cor_sentence.find(str(verbtext)) == -1:
                                                                    adder = adder - 7
                                                                    index_sen = int(sent_number) + adder
                                                                    cor_sentence = sentencelist[index_sen]
                                                                    if cor_sentence.find(str(verbtext)) == -1:
                                                                        adder = adder + 7
                                                                        index_sen = int(sent_number) + adder
                                                                        cor_sentence = sentencelist[index_sen]
                                                                        if cor_sentence.find(str(verbtext)) == -1:
                                                                            adder = adder - 8
                                                                            index_sen = int(sent_number) + adder
                                                                            cor_sentence = sentencelist[index_sen]
                                                                            if cor_sentence.find(str(verbtext)) == -1:
                                                                                adder = adder + 8
                                                                                index_sen = int(sent_number) + adder
                                                                                cor_sentence = sentencelist[index_sen]
                                                                                if cor_sentence.find(str(verbtext)) == -1:
                                                                                     print("ADDER ERROR")
                        # print(verbtext)
                        #print(cor_sentence)

                        # gather corresponding context
                        #cor_context = contextlist[index_sen]

                        # gather text_segment_id
                        text_segment = filename + "-fragment01"

                        # gather word offset
                        word_offset = child_of_child.get("ref")
                        last_index = word_offset.rfind(".")
                        word_offset = word_offset[last_index + 1 :]
                        word_offset = word_offset.replace(".", "")

                        if cor_sentence[0:1] == " ":
                            cor_sentence = cor_sentence[1:]

                        if cor_sentence[0:1] == " ":
                            cor_sentence = cor_sentence[1:]

                        # divide into test and train
                        # 70 percent train, 30 percent test
                        # 5757 training data
                        # 2467 test data
                        # TODO: UPDATE NUMERICAL VALUES HERE FOR TRAIN TEST DEV
                        #! 70 % TRAIN
                        #! 20 % TEST
                        #! 10 % DEV
                        if pos_tag is not "":
                            sent_no = sent_no + 1

                            output = (
                                text_segment
                                + " "
                                + str(sent_no)
                                + "\t"
                                + str(metaphor)
                                + "\t"
                                + cor_sentence
                                + "\t"
                                + str(pos_tag)
                                + "\t"
                                + str(int(word_offset)-1-letsofar)
                            )
                            
                            if sent_no <= train_test_border:  # was 33000
                                f.write(output + "\n")
                            elif sent_no > train_test_border:
                                g.write(output + "\n")


print("Sentences parsed: " + str(sent_no))
f.close()
g.close()
h.close()
