text = '<ol><li>item one</li><li>number two content</li><li>item automatically added text text text</li><li>point number 4</li></ol>'

params =  {"deckName": "test1",
            "modelName": "Basic-45797",
            "fields": {
                "Front": "This is an example of question front side",
                "Back": text
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                "statistic_dummies"
            ],
            "audio": [],
            "video": [],
            "picture": []
        }
