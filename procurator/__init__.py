"""
******************************************************************************
Record query and find the best match in a group of sentences.

This is the main module of the project, which in turn was created for a
voice-themed hackathon. There is sub-optimal logic, code that needs refactor
in this module.

Usage: __init__.py [--alg=<algorithm>]

Options:
  -h --help          .
  --alg=<algorithm>  Choose one from ["levenshtein_distance", "jaro_distance",
                       "damerau_levenshtein_distance"][Default: levenshtein_distance]
******************************************************************************
"""
import os
import jellyfish
from docopt import docopt
from prompt_toolkit import print_formatted_text, HTML, prompt
from bullet import Bullet
from procurator.db import get_user_nicks, get_user_knowledge
from procurator.record import rec_and_transcribe
from procurator.utils.logger import L


def get_user_name_prompt(usernames):
    return Bullet(
        bullet="*  ",
        prompt="Who do you want to talk to?",
        choices=usernames).launch()


def no_contrib_action(user_knowledge, user_name):
    if not user_knowledge:
        name = user_name
        print_formatted_text(HTML("<ansiyellow>Sadly, " \
                                  f"<i>[[{name}-Bot]]</i> has made no " \
                                  "contributions</ansiyellow>"))
        return prompt("Ask someone else? [y/n] ").lower() == "y"
    else:
        return "skip"


def fallback_audio_transcription(seconds=5):
    print_formatted_text(HTML("<ansigreen>What do you want to ask?</ansigreen>"))
    try:
        transcript = rec_and_transcribe(seconds)
    except Exception as e:
        transcript = None
        L.info("Something went wrong %s", str(e))
    corrected = None

    if not transcript:
        correct = False
    else:
        print_formatted_text(HTML(f"<ansiyellow>You said: <i>{transcript}</i></ansiyellow>"))
        correct = prompt(f"Does that look okay? [y/n] ").lower() == "y"

    if not correct:
        corrected = prompt("Damn, that happens. Please type your question this time: ")
    return corrected or transcript


def match_scores(query, haystack, ref, alg):
    return sorted([{"id_": id_,
                    "score": getattr(jellyfish, alg)(string, query)}
                   for id_, string in zip(ref, haystack)],
                  key=lambda el: el["score"])


def knowledge_filter(query, knowledge, alg="levenshtein_distance"):
    ids, questions, answers = zip(*knowledge)
    q_match_scores = match_scores(query, questions, ids, alg)[:3]
    a_match_scores = match_scores(query, answers, ids, alg)[:3]
    combined_scores = q_match_scores + a_match_scores
    best_match = min(combined_scores, key=lambda item: item["score"])
    return best_match["score"], answers[ids.index(best_match["id_"])]


def main():
    arguments = docopt(__doc__)
    algorithm = arguments["--alg"]
    users = get_user_nicks()
    users = [{"id": id, "name": name.strip()} for (id, name) in users]
    usernames = [user["name"] for user in users]
    user_name = get_user_name_prompt(usernames)
    user_knowledge = get_user_knowledge(users[usernames.index(user_name)]["id"])
    ask_someone_else = no_contrib_action(user_knowledge, user_name)

    if ask_someone_else and ask_someone_else != "skip":
        main()
    elif not ask_someone_else:
        return None

    transcription = fallback_audio_transcription()
    score, answer = knowledge_filter(transcription, user_knowledge, alg=algorithm)
    print_formatted_text(HTML("<ansigreen>We found an answer" \
                              f" with {(100 - score)}% match!</ansigreen>"))
    print_formatted_text(answer)
