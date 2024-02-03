import pprint
import os
import csv
from main import create_card, get_media, store_file
from pprint import pprint
from argparse import ArgumentParser

OBSIDIAN_FOLDER = "/Volumes/obs/notes/knowledge"
OBSIDIAN_FILES = "/Volumes/obs/notes/files"
DECK_NAME = 'GPT'

parser = ArgumentParser('anki automator')
parser.add_argument('-d', '--debug', help='debug mode, does not insert new flashcards to decks, just simulates', action = 'store_true')
parser.add_argument('-i', '--index', help='file index. Full name is FILEPATH+index (like "04")', type = str, default = "04")
parser.add_argument('-t', '--target_dec', help='which deck to import in', type = str, default = DECK_NAME)
parser.add_argument('-s', '--start', help='start account number in our account list(file)', type = int, default = 0)
parser.add_argument('-e', '--end', help='end account number in our account list(file)', type = int, default = 1000)
args = parser.parse_args()

print(args)
STARTER = 0 # args.start
LIMITER = 1000 # args.end06. Commonly Used Hypothesis Tests. Formulas and Examples
DEBUG_MODE = False # args.debug
# INDEX_COUNTER = "09. Looking for Links (Correlation and Regression)" # args.index
INDEX_COUNTER = "04" # args.index
# FILENAME = f"Statistic flashcards-{INDEX_COUNTER}.md"
# FILENAME = f"Probability-{INDEX_COUNTER}.md"
# FILENAME = f"DS flashcards-{INDEX_COUNTER}.md"
# FILENAME = f"SQL_{INDEX_COUNTER}.md"
FILENAME = f"GPT_{INDEX_COUNTER}.md"
# FILENAME = f"Sobes_tasks.txt"
# FILENAME = f"ML-02{INDEX_COUNTER}.md"
FILEPATH = os.path.join(OBSIDIAN_FOLDER, FILENAME)
# FILEPATH = f"Sobes_tasks.txt"
ERROR_FILENAME = f"errors_{INDEX_COUNTER}"
# MEDIA_DIR = get_media()
# print(f'{MEDIA_DIR=}')

def save_dict_line(file_name, item, sep = ";"):
    fields = item.keys()
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=sep)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow(item)

def load_source(filepath):
    with open (filepath) as f:
        s = f.read()
    return s

def split_source(raw_content):
    splitted = raw_content.split('Front:') # empty row as a deLIMITER between the cards
    """EACH flashcard should start with 'Front:'
    and information part is denoted with 'Back'"""
    return splitted

def parse_front(raw_front):
    front = raw_front.replace('**','').strip()
    return front

def create_flashcard_texts(list_of_blocks):
    flashcards_list = []
    for index, block in enumerate(list_of_blocks):
        back_text_listed = None
        """we splitted a raw text by 'Front:' string and now we have chunks of text"""
        print('-'*100)
        print(f'{index=}')

        if "Back" in block:
            splitted_card = block.split('Back:')
            front_part = splitted_card[0]
            back_text = splitted_card[1].split('\n')
            print(f'all parts found')
            # print(splitted_card)
        else:
            ite = {'index': index, "front": "" , "back" : '', "error": "'Back' not found!"}
            print(f'ERROR! {ite}')
            save_dict_line(f'errors{INDEX_COUNTER}.csv', ite)
            continue

        front = parse_front(front_part)
        print(f'{front=}')
        back = parse_back(back_text)
        print(f'{back=}')
        flashcards_list.append((front, back)) 
    return flashcards_list


def parse_back(back_text):
    formatted_text = "<ol>"
    li_counter = 0
    for index, item in enumerate(back_text):
        item = item.replace('**','')
        if "Back" in item:
            item = item.replace("Back:", "").replace('**','').strip()
            item = item.replace("Back of flashcard:", "").replace('**','').strip()
            if item == "":
                continue
        index +=1
        if item == "":
            continue
        item = item.strip()
        if "![[" in item:
            text_in_row = item.split('![[')[0]
            if text_in_row:
                li_item = f"<li>{text_in_row}</li>"
                if li_item != "!":
                    formatted_text += li_item
            img_filename = item.split('[[')[1].split(']]')[0]
            full_img_filepath = os.path.join("/Volumes/obs/notes/files", img_filename)
            print(f'{full_img_filepath=}, ready to download the image')
            store_file(full_img_filepath)
            print(f'image "{img_filename}" saved')
            img_html = f'<img src="{img_filename}">'
            li_item = f"<li>{img_html}</li>"
            formatted_text += li_item
            continue
        li_item = f"<li>{item}</li>"
        formatted_text += li_item
    formatted_text += "</ol>"
    formatted_text = formatted_text.replace('<li>- ','<li>')
    formatted_text = formatted_text.replace('<li></li>','')
    return formatted_text

def insert_single_card_into_deck():
    pass

def import_cards_into_anki(flashcard_texts):
    flashcard_texts = flashcard_texts[STARTER:LIMITER]
    for index, block in enumerate(flashcard_texts):
        front, back = block[0], block[1]
        print('-'*50)
        print(index, front)
        print(back)

        if not DEBUG_MODE:
            try:
                create_card(DECK_NAME, front, back)
            except:
                ite = {'index': index, 'front': front, "back" : back, 'error': "can not import"}
                save_dict_line(f'errors{INDEX_COUNTER}.csv', ite)

def main():
    raw_content = load_source(FILEPATH)
    splitted = split_source(raw_content)
    pprint(splitted[:3])
    flashcard_texts = create_flashcard_texts(splitted)
    pprint(flashcard_texts)
    import_cards_into_anki(flashcard_texts)


if __name__ == "__main__":
    main()
