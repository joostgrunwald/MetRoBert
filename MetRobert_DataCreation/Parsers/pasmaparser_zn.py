##############
#dependencies#
##############
import csv
from lxml import etree
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET
import os
import codecs

################
#USER INTERFACE#
################
print(" _______                                                                                                         ")                                                                                               
print("|       \                                                                                                        ") 
print("| $$$$$$$\ ______    _______  ______ ____    ______    ______    ______    ______    _______   ______    ______  ") 
print("| $$__/ $$|      \  /       \|      \    \  |      \  /      \  |      \  /      \  /       \ /      \  /      \ ") 
print("| $$    $$ \$$$$$$\|  $$$$$$$| $$$$$$\$$$$\  \$$$$$$\|  $$$$$$\  \$$$$$$\|  $$$$$$\|  $$$$$$$|  $$$$$$\|  $$$$$$\\") 
print("| $$$$$$$ /      $$ \$$    \ | $$ | $$ | $$ /      $$| $$  | $$ /      $$| $$   \$$ \$$    \ | $$    $$| $$   \$$") 
print("| $$     |  $$$$$$$ _\$$$$$$\| $$ | $$ | $$|  $$$$$$$| $$__/ $$|  $$$$$$$| $$       _\$$$$$$\| $$$$$$$$| $$      ") 
print("| $$      \$$    $$|       $$| $$ | $$ | $$ \$$    $$| $$    $$ \$$    $$| $$      |       $$ \$$     \| $$      ") 
print(" \$$       \$$$$$$$ \$$$$$$$  \$$  \$$  \$$  \$$$$$$$| $$$$$$$   \$$$$$$$ \$$       \$$$$$$$   \$$$$$$$ \$$      ") 
print("                                                     | $$                                                        ") 
print("                                                     | $$                                                        ") 
print("                                                      \$$                                                        ")
print("")
print("This program was written by Joost Grunwald for the Radboud university.")
print("The program parses the data of the dutch pasma corpus to make it usable for a context based neural network.")
print("")

##################
#GLOBAL VARIABLES#
##################
filenumber = 0 #will later on be incremented for new file
file_fragment = 0
sent_no = 0

directory = r'C:\Users\Josso\Documents\Radboud\corpus_alpino_parsed'
subdirectories = os.listdir(directory)

for directory_d2_first in subdirectories:
    #print(directory_d2_first)
    directory_d2 = directory + "\\" + directory_d2_first
    #for filename in os.listdir(directory_d2):
        #if filename.endswith(".xml"):
            #print(filename)

outputdirectory = r'C:\Users\Josso\Documents\Radboud\pasma_parsed_zn.txt'
f = codecs.open(outputdirectory, 'w', encoding='utf8')

f.write("bnc_file,bnc_file_n,fold_no,genre,id,min_context,partition,sentence_end_idx,sentence_number,sentence_offset,sentence_start_idx,subword_offset,text_segment_id,verb,word_offset,y,verb_lemma,sentence" + "\n")

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        adder = 0
        print(filename)
        filenumber = filenumber + 1
        file_fragment = file_fragment + 1
        filedirectory = directory + "\\" + filename
        genre = "news"
        parser = etree.XMLParser(ns_clean=True,remove_comments=True)
        tree = etree.parse(filedirectory,parser)
        root = tree.getroot()

        #<ptext ref="Aec2.txt">
        for filename_scrape in root.iter('ptext'):
            #only one occurence, not really a for loop, stores filename
            filename = filename_scrape.get('ref')
            
        filename = filename.replace(".txt","") #remove extension

        ############################################
        #PART 1: get Sentence, fulltext and context#
        ############################################
        fulltext = ""
        sentencelist = []
        contextlist = []
        for sent in root.iter('sent'):
            for child in sent:
                sentence = ""
                wordtext = ""
                for child_of_child in child:
                    if (child_of_child.get('s') == "UNKNOWN"):
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
                        if (temporary == ""):
                            if not str(child_of_child.text) == "None":
                                wordtext = wordtext + child_of_child.text
                                temporary = child_of_child.text
                        wordtext = wordtext + " "
                        sentence = wordtext
                            
                    #we need to make some adjustments to make the sentence be more correct again.
                if sentence != "" and sentence != "\n":                   
                    sentencelist.append(sentence)
        
        sentences_amount = len(sentencelist) - 1
        counter = 0
        previous_sen = ""
        
        #we format the sentence adding points when needed, to make it even more readable and hopefully get better results in our neural network (upgrade recall value)
        for sentence in sentencelist:
            counter = counter + 1
            if counter == 2 or counter == 3 or counter == 4:
                continue
            elif counter == 5: #8 july, changed this from 5 to 6
                #reset
                counter = 0
                continue
            elif counter == 1:
                index = sentencelist.index(sentence)
                context = ""
                #added begin
                if index <= sentences_amount:
                    con_sentence = sentencelist[index]
                    if con_sentence[len(con_sentence)-1:] == ".":
                        con_sentence = con_sentence + " "
                    elif con_sentence[len(con_sentence)-1:] == " ":
                        con_sentence = con_sentence[:len(con_sentence)-1]
                        if con_sentence[len(con_sentence)-1:] == ".":
                            con_sentence = con_sentence + " "
                        if con_sentence[len(con_sentence)-1:].isalpha():
                            con_sentence = con_sentence + ". "
                    elif con_sentence[len(con_sentence)-1:].isalpha():
                        con_sentence = con_sentence + ". "
                    if (con_sentence != previous_sen):
                        context = context + con_sentence
                        previous_sen = con_sentence
                #added end
                if index + 1 <= sentences_amount:
                    con_sentence = sentencelist[index+1]
                    if con_sentence[len(con_sentence)-1:] == ".":
                        con_sentence = con_sentence + " "
                    elif con_sentence[len(con_sentence)-1:] == " ":
                        con_sentence = con_sentence[:len(con_sentence)-1]
                        if con_sentence[len(con_sentence)-1:] == ".":
                            con_sentence = con_sentence + " "
                        if con_sentence[len(con_sentence)-1:].isalpha():
                            con_sentence = con_sentence + ". "
                    elif con_sentence[len(con_sentence)-1:].isalpha():
                        con_sentence = con_sentence + ". "
                    if (con_sentence != previous_sen):
                        context = context + con_sentence
                        previous_sen = con_sentence
                if index + 2 <= sentences_amount:
                    con_sentence = sentencelist[index+2]
                    if con_sentence[len(con_sentence)-1:] == ".":
                        con_sentence = con_sentence + " "
                    elif con_sentence[len(con_sentence)-1:] == " ":
                        con_sentence = con_sentence[:len(con_sentence)-1]
                        if con_sentence[len(con_sentence)-1:] == ".":
                            con_sentence = con_sentence + " "
                        if con_sentence[len(con_sentence)-1:].isalpha():
                            con_sentence = con_sentence + ". "
                    elif con_sentence[len(con_sentence)-1:].isalpha():
                        con_sentence = con_sentence + ". "
                    if (con_sentence != previous_sen):
                        context = context + con_sentence
                        previous_sen = con_sentence
                if index + 3 <= sentences_amount:
                    con_sentence = sentencelist[index+3]
                    if con_sentence[len(con_sentence)-1:] == ".":
                        con_sentence = con_sentence + " "
                    elif con_sentence[len(con_sentence)-1:] == " ":
                        con_sentence = con_sentence[:len(con_sentence)-1]
                        if con_sentence[len(con_sentence)-1:] == ".":
                            con_sentence = con_sentence + " "
                        if con_sentence[len(con_sentence)-1:].isalpha():
                            con_sentence = con_sentence + ". "
                    elif con_sentence[len(con_sentence)-1:].isalpha():
                        con_sentence = con_sentence + ". "
                    if (con_sentence != previous_sen):
                        context = context + con_sentence
                        previous_sen = con_sentence
                if index + 4 <= sentences_amount:
                    con_sentence = sentencelist[index+4]
                    if con_sentence[len(con_sentence)-1:] == ".":
                        con_sentence = con_sentence + " "
                    elif con_sentence[len(con_sentence)-1:] == " ":
                        con_sentence = con_sentence[:len(con_sentence)-1]
                        if con_sentence[len(con_sentence)-1:] == ".":
                            con_sentence = con_sentence + " "
                        if con_sentence[len(con_sentence)-1:].isalpha():
                            con_sentence = con_sentence + ". "
                    elif con_sentence[len(con_sentence)-1:].isalpha():
                        con_sentence = con_sentence + ". "
                    if (con_sentence != previous_sen):
                        context = context + con_sentence
                        previous_sen = con_sentence
                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)
                contextlist.append(context)

        #for context in contextlist:
            #print(context)

        ################################################
        #PART 2: get verb, verb lemma and bool metaphor#
        ################################################
        #print(".cvs syntax output:")
        output = ""
        for sent in root.iter('sent'):
            for child in sent:
                for child_of_child in child:               
                    metaphor = 0
                    verbtext = ""
                    verb_lemma = ""
                    if (child_of_child.get('s') == "UNKNOWN"):
                        for child3 in child_of_child:
                            if ("N(" in child3.get('pos')):
                                #gather verb lemma
                                verb_lemma = child3.get('lem')

                                #gather verb
                                for child4 in child3:
                                    verbtext = child4.text
                                    metaphor = 1
                                if (verbtext == ""):
                                    verbtext = child3.text
                                    metaphor = 0

                                #gather sentence number
                                sent_number = sent.get('id')

                                #gather corresponding sentence
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
                                        if cor_sentence.find(verbtext) == - 1:
                                            adder = adder + 3
                                            index_sen = int(sent_number) + adder
                                            cor_sentence = sentencelist[index_sen]
                                            if cor_sentence.find(verbtext) == - 1:
                                                adder = adder - 4
                                                index_sen = int(sent_number) + adder
                                                cor_sentence = sentencelist[index_sen]
                                                if cor_sentence.find(verbtext) == - 1:
                                                    adder = adder + 4
                                                    index_sen = int(sent_number) + adder
                                                    cor_sentence = sentencelist[index_sen]                              

                                #gather corresponding context
                                cor_context = contextlist[index_sen]

                                #integrate alpino object/subject
                                folder_name = filename
                                folder_name = folder_name.replace(".xml","")
                                folder_name = folder_name.replace("-fa","")
                                folder_name = folder_name + "_sen.txt.alpinoxml"
                                folder_name = directory + "\\" + folder_name
                                subject = ""
                                objec = ""
                                subjectlem = ""
                                objectlem = ""
                                for filename_2 in os.listdir(folder_name):
                                    con_sentnumber = str(index_sen + 1) #because we count from 0 but pasma from 1
                                    correctfile = filename + "_" + con_sentnumber + ".xml.txt"
                                    correctfile_2 = filename + "_" + str(int(con_sentnumber) + 1) + ".xml.txt"
                                    correctfile_3 = filename + "_" + str(int(con_sentnumber) - 1) + ".xml.txt"
                                    try_again = False
                                    if filename_2 == correctfile or filename_2 == correctfile_2 or filename_2 == correctfile_3:
                                        #getting directory
                                        full_directory = folder_name + "\\" + filename_2
                                        context = codecs.open(full_directory, 'r', encoding='ISO-8859-1').readlines()
                                    
                                        #print(context)
                                        #print("verb")
                                        #print(verbtext)
                                        #sanitizing input and iterating it

                                #gather text_segment_id
                                text_segment = filename + "-fragment01"

                                #gather word offset
                                word_offset = child_of_child.get('ref')
                                last_index = word_offset.rfind('.')
                                word_offset = word_offset[last_index+1:]
                                word_offset = word_offset.replace(".","")

                                #gather sentence start id
                                sen_start_index = cor_context.find(cor_sentence)

                                #gather sentence end id
                                if index_sen + 1 <= len(sentencelist):
                                    next_sentence = sentencelist[index_sen + 1]
                                    sen_end_index = cor_context.find(next_sentence) - 1
                                    if sen_end_index == -2: #not found so last sentence of context
                                        sen_end_index = len(cor_context)
                                else:
                                    sen_end_index = len(cor_context)

                                #sentence offset
                                sen_offset = sent_number

                                #divide into test and train
                                #70 percent train, 30 percent test
                                #5757 training data
                                #2467 test data
                                if sent_no > 9600:
                                    sub_offset = "0" #1 for train 0 for test
                                    partition = "test"
                                    word_id = text_segment + "_" + sent_number + "_" + sen_offset
                                else:
                                    sub_offset = "1"
                                    partition = "train"
                                    #gather id
                                    word_id = text_segment + "_" + sent_number + "_" + sen_offset + "_" + word_offset + "_" + "1" + "_" + verbtext

                                if cor_sentence.find(",") != -1 or cor_sentence.find(";") != -1:
                                    cor_sentence = '"' + cor_sentence + '"'
                                                                    
                                if cor_context.find("  ") != -1:
                                    cor_context = cor_context.replace("  "," ")

                                if cor_sentence[0:1] == " ":
                                    cor_sentence = cor_sentence[1:]

                                #print output in csv form
                                sent_no = sent_no + 1
                                output = filename + "," + str(file_fragment) + "," + str(filenumber) + "," + genre + "," + word_id + "," + '"' + cor_context + '"' + "," + partition + "," + str(sen_end_index) + "," + sent_number + "," + sen_offset 
                                output = output + "," + str(sen_start_index) + "," + sub_offset + "," + text_segment + "," + verbtext + "," + word_offset + "," + str(metaphor)
                                output = output + "," + verb_lemma + "," + cor_sentence
                                f.write(output + "\n")
                                
                    elif str(child_of_child.get('pos')) != "None" and ("N(" in child_of_child.get('pos')):
                        #gather verb lemma
                        verb_lemma = child_of_child.get('lem')
                        
                        #gather verb
                        for child3 in child_of_child:
                            verbtext = child3.text
                            metaphor = 1
                        if (verbtext == ""):
                            verbtext = child_of_child.text
                            metaphor = 0

                        #gather sentence number
                        sent_number = sent.get('id')

                        #gather corresponding sentence
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
                                if cor_sentence.find(verbtext) == - 1:
                                    adder = adder + 3
                                    index_sen = int(sent_number) + adder
                                    cor_sentence = sentencelist[index_sen]
                                    if cor_sentence.find(verbtext) == - 1:
                                        adder = adder - 4
                                        index_sen = int(sent_number) + adder
                                        cor_sentence = sentencelist[index_sen]
                                        if cor_sentence.find(verbtext) == - 1:
                                            adder = adder + 4
                                            index_sen = int(sent_number) + adder
                                            cor_sentence = sentencelist[index_sen]
                        #print(verbtext)
                        #print(cor_sentence)

                        #integrate alpino object/subject
                        folder_name = filename
                        folder_name = folder_name.replace(".xml","")
                        folder_name = folder_name.replace("-fa","")
                        folder_name = folder_name + "_sen.txt.alpinoxml"
                        folder_name = directory + "\\" + folder_name
                        subject = ""
                        objec = ""
                        subjectlem = ""
                        objectlem = ""
                        for filename_2 in os.listdir(folder_name):
                            con_sentnumber = str(index_sen + 1) #because we count from 0 but pasma from 1
                            correctfile = filename + "_" + con_sentnumber + ".xml.txt"
                            correctfile_2 = filename + "_" + str(int(con_sentnumber) + 1) + ".xml.txt"
                            correctfile_3 = filename + "_" + str(int(con_sentnumber) - 1) + ".xml.txt"
                            try_again = False
                            if filename_2 == correctfile or filename_2 == correctfile_2 or filename_2 == correctfile_3:
                                #getting directory
                                full_directory = folder_name + "\\" + filename_2
                                context = codecs.open(full_directory, 'r', encoding='ISO-8859-1').readlines()
                            
                                #print(context)
                                #print("verb")
                                #print(verbtext)
                                #sanitizing input and iterating it

                        #gather corresponding context
                        cor_context = contextlist[index_sen]

                        #gather text_segment_id
                        text_segment = filename + "-fragment01"

                        #gather word offset
                        word_offset = child_of_child.get('ref')
                        last_index = word_offset.rfind('.')
                        word_offset = word_offset[last_index+1:]
                        word_offset = word_offset.replace(".","")

                        #gather sentence start id
                        sen_start_index = cor_context.find(cor_sentence)

                        #gather sentence end id
                        if index_sen + 1 < len(sentencelist):
                            next_sentence = sentencelist[index_sen + 1]
                            sen_end_index = cor_context.find(next_sentence) - 1
                            if sen_end_index == -2: #not found so last sentence of context
                                sen_end_index = len(cor_context)
                        else:
                            sen_end_index = len(cor_context)

                        #divide into test and train
                        #70 percent train, 30 percent test
                        #5757 training data
                        #2467 test data
                        if sent_no > 10000:
                            sen_offset = "0"
                            sub_offset = "0" #1 for train 0 for test
                            partition = "test"
                            word_id = text_segment + "_" + sent_number + "_" + sen_offset
                        else:
                            sen_offset = sent_number
                            sub_offset = "1"
                            partition = "train"
                            #gather id
                            word_id = text_segment + "_" + sent_number + "_" + sen_offset + "_" + word_offset + "_" + "1" + "_" + verbtext

                        if cor_sentence.find(",") != -1 or cor_sentence.find(";") != -1:
                            cor_sentence = '"' + cor_sentence + '"'
                            
                        if cor_context.find("  ") != -1:
                            cor_context = cor_context.replace("  "," ")

                        if cor_sentence[0:1] == " ":
                            cor_sentence = cor_sentence[1:]

                        #trying to fix spaces at the end of strings.
                        if cor_sentence[-1:] == " ":
                            cor_sentence = cor_sentence[0:len(cor_sentence)-1]

                        #adjust hoofdletters
                        if verb_lemma[0:1].islower() and verbtext[0:1].isupper():
                            verbtext = verbtext.lower()
                            
                        #print output in csv form
                        sent_no = sent_no + 1
                        output = filename + "," + str(file_fragment) + "," + str(filenumber) + "," + genre + "," + word_id + "," + '"' + cor_context + '"' + "," + partition + "," + str(sen_end_index) + "," + sent_number + "," + sen_offset 
                        output = output + "," + str(sen_start_index) + "," + sub_offset + "," + text_segment + "," + verbtext + "," + word_offset + "," + str(metaphor)
                        output = output + "," + verb_lemma + "," + cor_sentence
                        f.write(output + "\n")
            
print("Sentences parsed: " + str(sent_no))
f.close()
