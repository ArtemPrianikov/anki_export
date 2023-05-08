import pprint
import os
import csv
from main import create_card

with open ('raw_text.txt') as f:
    s = f.read()

def save_dict_line(file_name, item, sep = ";"):
    fields = item.keys()
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=sep)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow(item)

splitted = s.split('\n\n')
splitted  = splitted[:]
for index, i in enumerate(splitted):
    print('-'*100)
    print(f'{index=}')
    splitted_card = i.split('\n')
    front = splitted_card[0].replace('Front: ','').replace('Front of flashcard: ','')
    print(front)
    formatted_text = "<ol>"
    li_counter = 0
    for index, item in enumerate(splitted_card[1:]):
        if "Back" in item:
            # item = item.replace('Back of flashcard: ','').replace("Back: ", "")
            item = item.replace("Back:", "").strip()
            item = item.replace("Back of flashcard:", "").strip()
            if item == "":
                print('!'*50)
                continue
        index +=1
        if item == "":
            continue
        li_item = f"<li>{item}</li>"
        formatted_text += li_item
        print(index)
        print(item)
    formatted_text += "</ol>"
    print(formatted_text)
    print()
    print()
    try:
        create_card('mystat', front, formatted_text)
    except:
        ite = {'front': front, "back" : formatted_text}
        save_dict_line('errors.csv', ite)

