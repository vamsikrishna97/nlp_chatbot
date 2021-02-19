# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os
import goslate

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('LANG SEARCH')
        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)

            try:
                gs = goslate.Goslate()
                final  = gs.translate(query_lang, 'en')
                print(final)
                out_row = wals_data[wals_data["Name"] == final].to_dict("records")

                if len(out_row) > 0:
                    out_row = out_row[0]
                    out_text = "%s भाषा %s परिवार से संबंधित है।\nइसका जीनस %s है।\nइसका ISO कोड %s है।" % (query_lang, out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = "क्षमा करें! हमारे पास %s भाषा के रिकॉर्ड नहीं हैं।" % query_lang)
            except:
                dispatcher.utter_message(text = "Google API से संपर्क करने में असमर्थ, पुनः प्रयास करें।")

        return []

class ActionCountrySearch(Action):

    def name(self) -> Text:
        return "action_country_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        countries_languages_path = os.path.join("data", "cldf-datasets-wals-014143f", "created", "lang_country_info.csv")
        countries_languages_data = pd.read_csv(countries_languages_path)

        entities = list(tracker.get_latest_entity_values("country"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().title()
            print(query_lang)

            try:
                gs = goslate.Goslate()
                final  = gs.translate(query_lang, 'en')
                print(final)
                out_row = countries_languages_data[countries_languages_data["country_name"] == final].to_dict("records")

                if len(out_row) > 0:
                    languages = []
                    for i in range(len(out_row)):
                        languages.append(out_row[i]["name"])
                    print(languages)
                    out_text = "%s की भाषा/एँ: \n%s" % (query_lang, ", ".join(languages))
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = "क्षमा करें! हमारे पास %s देश के रिकॉर्ड नहीं हैं।" % query_lang)
            except:
                dispatcher.utter_message(text = "Google API से संपर्क करने में असमर्थ, पुनः प्रयास करें।")

        return []

class FeedbackReply(Action):

    def name(self) -> Text:
        return "feedback_reply"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text = "क्या इससे आपको मदद मिली, बेटा?")
        return []

class TLFLanguages(Action):

    def name(self) -> Text:
        return "action_tlf_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        data_path = os.path.join("data", "linguistic_bg_students.csv")
        df = pd.read_csv(data_path)
        df = df[df['Name'].notnull()]
        df['L1 - Mother tongue']= df['L1 - Mother tongue'].str.lower()
        entities = list(tracker.get_latest_entity_values("language"))
        print(entities)
        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().title()
            print(query_lang)
            try:
                out_row = df[df['L1 - Mother tongue'] == query_lang ]
                if len(out_row) > 0:
                    people = []
                    for i in range(len(out_row)):
                        people.append(out_row[i]["Name"])
                    print(people)
                    out_text = "%s की भाषा/एँ: \n%s" % (query_lang, ", ".join(languages))
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = 'could not find {}'.format(query_lang))

            except:
                dispatcher.utter_message(text = "Google API से संपर्क करने में असमर्थ, पुनः प्रयास करें।")


        return []
