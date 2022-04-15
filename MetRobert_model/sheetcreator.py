import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

import os

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)

client = gspread.authorize(creds)

out = client.create('MetRubert output')

out.share('commercialtwots@gmail.com', perm_type='user', role='writer')

# get current location folder
location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

previous_sentence = None
pos_list = []
met_list = []

sentences = []

with open(os.path.join(location, 'output.tsv'), mode='r', encoding='utf-8') as output:
    for line in output:
        if line[0:5] != "index":
            splitted = line.split("\t")

            sentence = splitted[1]
            
            if sentence != previous_sentence and previous_sentence != None:

                #TODO: wrapup
                print(previous_sentence)
                print(met_list)
                print(pos_list)
                
                sentences.append(sentence)
                
                previous_sentence = sentence
                pos_list = []
                met_list = []

            else:
                #append pos tag
                pos = splitted[2]
                index = splitted[3]
                pos_list.append((index, pos))

                #append metaphor
                met = splitted[5]
                if met.find("1") != -1 and met.find("-1") == -1:
                    met_list.append(index)

                previous_sentence = sentence

print(sentences)          
# TODO: open output.tsv file

# TODO: save panda dataframe to google sheets

# TODO: make metpahors bold, use background color for pos tags, rewrite softmax to confidence

# sheet = client.open("MetRubert_Sheets").sheet1  # Open the spreadhseet

# data = sheet.get_all_records()  # Get a list of all records
# print(data)

# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell

# insertRow = ["hello", 5, "red", "blue"]
# sheet.appendRow(insertRow, 4)  # Insert the list as a row at index 4

# sheet.update_cell(2,2, "CHANGED")  # Update one cell

# numRows = sheet.row_count  # Get the number of rows in the sheet
