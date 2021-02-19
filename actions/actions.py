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
#import goslate
from google_trans_new import google_translator
import re

import random

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
                translator = google_translator()
                #gs = goslate.Goslate()
                #final  = gs.translate(query_lang, 'en')
                final = translator.translate(query_lang,lang_tgt='en')
                final = final.lower()
                final = re.sub("[^a-zA-Z]+", "", final)

                #print(len(re.sub("[^a-zA-Z]+", "", final)))
                #print(type(final))
                #print(final == 'hindi')
                out_row = wals_data[wals_data["Name"].str.lower() == final].to_dict("records")
                #print(wals_data[wals_data["Name"]=='Hindi'])
                #print(out_row)

                if len(out_row) > 0:
                    out_row = out_row[0]
                    out_text = "%s भाषा %s परिवार से संबंधित है।\nइसका जीनस %s है।\nइसका ISO कोड %s है।" % (query_lang, out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = "क्षमा करें! हमारे पास %s भाषा के रिकॉर्ड नहीं हैं।" % query_lang)
            except:
                dispatcher.utter_message(text = "बेटा, System Error के लिए माफी माँगता हूँ। कुछ समय बाद प्रयास करें।")

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
                #gs = goslate.Goslate()
                translator = google_translator()
                #final  = gs.translate(query_lang, 'en')
                #print(final)
                final = translator.translate(query_lang,lang_tgt='en')
                final = final.lower()
                final = re.sub("[^a-zA-Z]+", "", final)
                print(final)
                out_row = countries_languages_data[countries_languages_data["country_name"].str.lower() == final].to_dict("records")

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
                dispatcher.utter_message(text = "बेटा, System Error के लिए माफी माँगता हूँ। कुछ समय बाद प्रयास करें।")

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
        print('TLF LANGUAGES')
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
            translator = google_translator()
            final = translator.translate(query_lang,lang_tgt='en')
            final = final.lower()
            final = re.sub("[^a-zA-Z]+", "", final)
            print(final)
            try:
                out_row = df[df['L1 - Mother tongue'] == final ]['Name'].tolist()
                print(out_row)
                if len(out_row) > 0:
                    out_text = 'बेटा! TLF में इन लोग की मातृ भाषा {} हैं \n'.format(query_lang)
                    for i, val in enumerate(out_row,1):
                        out_text += '{}. {} \n'.format(i,val)
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = 'बेटा! TLF में {} मातृ भाषा वला कोइ नहिं'.format(query_lang))

            except:
                dispatcher.utter_message(text = "Google API से संपर्क करने में असमर्थ, पुनः प्रयास करें।")


        return []

class ActionExampleLanguage(Action):

    def name(self) -> Text:
        return "action_example_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('EXAMPLE SEARCH')
        data_path_languages = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "language_names.csv")
        wals_data_languages = pd.read_csv(data_path_languages)
        entities = list(tracker.get_latest_entity_values("language"))

        data_path_examples = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "examples.csv")
        wals_data_examples = pd.read_csv(data_path_examples)

        if len(entities) > 0:
            query_lang = entities.pop()
            print(query_lang)

        try:
            translator = google_translator()
            english_translation  = translator.translate(query_lang,lang_tgt='en').lower()
            english_translation  = re.sub("[^a-zA-Z]+", "", english_translation).capitalize()
            print(english_translation)
            out_row = wals_data_languages[wals_data_languages["Name"] == english_translation].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_row["Language_ID"]
                examples_out_row = wals_data_examples[wals_data_examples["Language_ID"] == out_row["Language_ID"]].to_dict("records")

                if len(examples_out_row) > 0:
                    examples_out_row = random.choice(examples_out_row)
                    out_text = "बेटा! %s भाषा का एक उदाहरण कुछ इस तरह है: %s\n जिसका हिंदी में अनुवाद होता है: %s" % (query_lang, examples_out_row["Primary_Text"], translator.translate(examples_out_row["Translated_Text"],lang_tgt='hi'))
                    dispatcher.utter_message(text = out_text)
                else:
                    dispatcher.utter_message(text = "क्षमा करें! हमारे पास %s भाषा के रिकॉर्ड नहीं हैं।" % query_lang)
        except:
            dispatcher.utter_message(text = "बेटा, System Error के लिए माफी माँगता हूँ। कुछ समय बाद प्रयास करें।")

        return []
