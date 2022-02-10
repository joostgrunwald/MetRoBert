##############
#dependencies#
##############
import csv
from lxml import etree
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET
import io
import os

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
filenumber = 1 #will later on be incremented for new file
filename = ""
file_fragment = 1
genre = "news"
parser = etree.XMLParser(ns_clean=True,remove_comments=True)
directory = r'C:\Users\Josso\Documents\Radboud\corpus_parsed'
for filename2 in os.listdir(directory):
    if filename2.endswith(".xml"):
        print(filename2)
        filedirectory = directory + "\\" + filename2
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
                    sentence = sentence.replace(" . ",".")
                    sentence = sentence.replace(" ,",",")
                    sentence = sentence.replace(" :",":")
                    sentence = sentence.replace("( ","(")
                    sentence = sentence.replace(" )",")")
                    sentence = sentence.replace(" ;",";")
                    sentencelist.append(sentence)

        outputdirectory = directory + "\\" + filename + "_sen" + ".txt"
        f = io.open(outputdirectory, "w", encoding="utf-8")
        for sentence in sentencelist:
            f.write(sentence + "\n")
        f.close()
        
        
