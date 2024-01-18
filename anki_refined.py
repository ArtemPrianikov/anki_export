
import os
import csv
import json
import urllib.request
from argparse import ArgumentParser

# Constants
OBSIDIAN_FOLDER = "/Volumes/obs/notes/knowledge"
OBSIDIAN_FILES = "/Volumes/obs/notes/files"
DECK_NAME = 'mystat2'

def save_dict_line(file_name: str, item: dict, sep: str = ";") -> None:
    fields = item.keys()
    file_exists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=sep)
        if not file_exists:
            writer.writeheader()
        writer.writerow(item)

def load_source(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()

def split_source(raw_content: str) -> list:
    return raw_content.split('Front:')

def parse_front(raw_front: str) -> str:
    return raw_front.replace('**', '').strip()

def parse_back(back_text: list) -> str:
    formatted_text = "<ol>"
    for item in back_text:
        item = item.replace('**', '').strip()
        if item:
            formatted_text += f"<li>{item}</li>"
    formatted_text += "</ol>"
    return formatted_text

def create_flashcard_texts(list_of_blocks: list) -> list:
    flashcards_list = []
    for block in list_of_blocks:
        if "Back" in block:
            splitted_card = block.split('Back:')
            front = parse_front(splitted_card[0])
            back = parse_back(splitted_card[1].split('\n'))
            flashcards_list.append((front, back))
    return flashcards_list

def main():
    parser = ArgumentParser('anki automator')
    parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
    parser.add_argument('-i', '--index', help='file index', type=str, default="04")
    parser.add_argument('-t', '--target_dec', help='target deck', type=str, default=DECK_NAME)
    args = parser.parse_args()

    raw_content = load_source(os.path.join(OBSIDIAN_FOLDER, f"Probability-{args.index}.md"))
    flashcard_texts = create_flashcard_texts(split_source(raw_content))

    # TODO: Insert the flashcards into Anki (not shown in provided code snippet)

if __name__ == "__main__":
    main()
