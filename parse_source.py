import pprint
import os
import csv
from main import create_card
from pprint import pprint

index_counter = 3
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

# splitted = s.split('\n\n') # empty row as a delimiter between the cards
#    """we splitted a raw text by empty row and now we have chunks of text. they can have
#    different structure. Sometimes they can have 'Front' and 'Back' headers, and sometimes not"""
splitted = s.split('Front:') # empty row as a delimiter between the cards
"""it seems this text is using "Front"-"Back" structure. EACH flashcard should start with 'Front:'
and information part is denoted with 'Back'"""
splitted  = splitted[starter:limiter]
for index, i in enumerate(splitted):
    back_text_listed = None
    """we splitted a raw text by 'Front:' string and now we have chunks of text"""
    
    print('-'*100)
    print(f'{index=}')

    if "Back" in i:
        splitted_card = i.split('Back:')
        front_part = splitted_card[0]
        back_text = splitted_card[1].split('\n')
        print(f'all parts found')
        # print(splitted_card)
    else:
        ite = {'index': index, "front": "" , "back" : '', "error": "'Back' not found!"}
        print(f'ERROR! {ite}')
        save_dict_line(f'errors{index_counter}.csv', ite)
        continue

    front = front_part.strip()
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
            ite = {'index': index, 'front': front, "back" : formatted_text, 'error': "can not import"}
            save_dict_line(f'errors{index_counter}.csv', ite)

