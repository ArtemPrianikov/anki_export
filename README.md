
# Anki Markdown Importer

Easily transform structured markdown files into Anki decks.

## Features

- **Markdown Parsing:** Convert structured Markdown files with flashcards denoted by 'Front:' and 'Back:' labels.
- **HTML Formatting:** Transform back content into an HTML-like structure using ordered lists.
- **Image Handling:** Manage embedded images and links from the Markdown and ensure they're correctly formatted for Anki.
- **Anki Integration:** Seamlessly add parsed flashcards to specified Anki decks.
- **Error Logging:** Log errors during the import process to a CSV file for review.

## Usage

```bash
python anki.py [OPTIONS]
```

### Options for `anki.py`:

- `-d`, `--debug`: Run in debug mode. This simulates the process without actually inserting new flashcards to decks.
- `-i`, `--index`: File index to process. The full name is constructed using FILEPATH + index (e.g., "04").
- `-t`, `--target_dec`: Specifies which Anki deck to import into. Default is 'mystat2'.
- `-s`, `--start`: Starting account number in the account list (file). Default is 0.
- `-e`, `--end`: Ending account number in the account list (file). Default is 1000.

### Additional Utilities (`main.py`):

- **AnkiConnect Integration:** The script uses the AnkiConnect plugin to interact with Anki. Ensure you have AnkiConnect installed in Anki.
- **Card Creation:** Create cards in Anki programmatically.
- **Media Handling:** Retrieve the media directory path and store media files in Anki.

### Options for `main.py`:

- `-i`, `--info`: Provides information.
- `-c`, `--create`: Indicates that cards should be created.

## Requirements

- Python 3.x
- Anki with AnkiConnect plugin installed.
- Ensure both `anki.py` and `main.py` are in the same directory.

