from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.request import urlopen

import json

def calculateBoWVectors(arguments, webpage):
    """
    Calculate Bag of Words vectors using sklearn

    :param arguments: all arguments submitted by the participants as one string
    :param webpage: webpage contents to compare against as one string
    :return: two vectors representing word frequencies.
    """
    vectorizer = CountVectorizer(strip_accents='unicode')
    X = vectorizer.fit_transform([arguments, webpage])

    return X.toarray()


def getWebPageText(url):
    """
    Get the text contents of the web page at the specified URL.

    :param url: web page to get the contents of
    :return: contents of the web page as plain text.
    """
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # Delete tags
    for script in soup(["script", "style", "header"]):
        script.extract()

    # Get text, break into lines, remove leading/trailing blank spaces & blank lines
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    text = '\n'.join(line for line in lines if line)

    return text


def importArgs(file):
    """
    Import submitted arguments and group arguments per participant

    :param file: File to import the arguments from.
    :return: Dictionary with the arguments grouped by participant as one string.
    """
    argsPerParticipant = {}
    with open(file) as args_file:
        for line in args_file:
            json_entry = json.loads(line)
            argsPerParticipant[json_entry['_id']] = ' '.join(json_entry['args'])

    return argsPerParticipant


def importClicksFromLogs(logFiles):
    """
    Import clicked search results from log files,
    grouped per participant.

    :param logFiles: An array of strings pointing to log files.
    :return: Clicked web search results
    """
    clicksPerParticipant = {}

    for file in logFiles:
        with open(file) as logFile:
            logs_json = json.load(logFile)
            for log in logs_json:
                if log['eventDetails']['type'] == "mouseClick" and (log['eventDetails']['name'] == 'SEARCH_RESULT_CLICKED_AUX' or log['eventDetails']['name'] == 'SEARCH_RESULT_CLICKED'):
                    prolificID = log['applicationSpecificData']['prolificID']
                    url = log['metadata'][1]['value']
                    if prolificID not in clicksPerParticipant:
                        clicksPerParticipant.update({prolificID: [url]})
                    else:
                        clicksPerParticipant[prolificID].append(url)

    return clicksPerParticipant

if __name__ == '__main__':

    # Log files to extract the search result clicks from
    logFiles = ["/home/mike/git/bbt-analysis/data/in/logs-list.log"]
                # "/home/mike/git/bbt-analysis/data/in/logs-grid.log"]
                # "/home/mike/git/bbt-analysis/data/in/logs-ilsp.log",
                # "/home/mike/git/bbt-analysis/data/in/logs-sa.log"]
    clicksPerParticipant = importClicksFromLogs(logFiles)
    argsPerParticipant = importArgs("/home/mike/git/bbt-analysis/data/in/args.json")

    # Open a file for wrtiting the cosine similarities to
    file = open("/home/mike/git/bbt-analysis/data/out/listReliance.csv", "w")
    file.write("prolificID,maxSimilarity\n")
    for (participant, urls) in clicksPerParticipant.items():
        if participant is not None:
            highest = 0
            # Check the similarity between each url and submitted arguments
            for url in urls:
                try:
                    cos_sim = cosine_similarity(calculateBoWVectors(argsPerParticipant[participant], getWebPageText(url)))[0][1]
                    highest = highest if cos_sim < highest else cos_sim
                except:
                    print("[Web page inaccessible] Participant: " + participant + ", url: " + url + "")
            file.write(participant + "," + str(cos_sim) + "\n")
    file.close()

