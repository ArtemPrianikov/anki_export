import pprint
import os
import csv
from main import create_card
from pprint import pprint

index_counter = 2
starter = 0
limiter = 300
debug_mode = False
deck_name = 'mystat2'
with open (f'raw_text{index_counter}.txt') as f:
    s = f.read()

def save_dict_line(file_name, item, sep = ";"):
    fields = item.keys()
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=sep)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow(item)

splitted = s.split('\n\n') # empty row as a delimiter between the cards
splitted  = splitted[starter:limiter]
for index, i in enumerate(splitted):
    back_text_listed = None
    """we splitted a raw text by empty row and now we have chunks of text. they can have
    different structure. Sometimes they can have 'Front' and 'Back' headers, and sometimes not"""
    
    print('-'*100)
    print(f'{index=}')

    if "Front:" in i:
        print('it seems this text is using "Front"-"Back" structure')
        if "Back" in i:
            splitted_card = i.split('Back:')
            back_text = splitted_card[1].split('\n')
        else:
            splitted_card = i.split('\n')
            back_text = splitted_card[1:]
        print(splitted_card)
    else:
        splitted_card = i.split('\n')
        back_text = splitted_card[1:]

    front = splitted_card[0].replace('Front:','').replace('Front of flashcard:','').strip()
    print(f'{front=}')

    formatted_text = "<ol>"
    li_counter = 0

    for index, item in enumerate(back_text):
        if "Back" in item:
            # item = item.replace('Back of flashcard: ','').replace("Back: ", "")
            item = item.replace("Back:", "").strip()
            item = item.replace("Back of flashcard:", "").strip()
            if item == "":
                # print('!'*50)
                continue
        index +=1
        if item == "":
            continue
        item = item.strip()
        li_item = f"<li>{item}</li>"
        formatted_text += li_item
        # print(index)
        # print(item)
    formatted_text += "</ol>"
    print(formatted_text)
    print()
    print()
    if not debug_mode:
        try:
            create_card(deck_name, front, formatted_text)
        except:
            ite = {'front': front, "back" : formatted_text}
            save_dict_line(f'errors{index_counter}.csv', ite)

