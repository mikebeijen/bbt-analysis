import json
from urllib.parse import unquote
import re

def importLogs(file):
    """
    Import the raw JSON logs as a dictionary.

    :param file: file containing the raw logs to import
    :return: imported logs as JSON
    """
    with open(file) as log_file:
        logs_json = json.load(log_file)
        return logs_json


def groupLogsPerSubmission(logs):
    """
    Group all logs by the prolific id of the participant.

    :param logs: the raw, ungrouped logs
    :return: logs grouped per participant
    """
    submissionsGrouped = {}
    for log in logs:
        prolificid = log['applicationSpecificData']['prolificID']
        if prolificid not in submissionsGrouped:
            submissionsGrouped.update({prolificid: [log]})
        else:
            submissionsGrouped[prolificid].append(log)
    return submissionsGrouped


def calculateMetricsPerSubmission(submission, submissionTime, submissionLogs):
    """
    calculate search behavior metrics from the logs
    of one participant. SubmissionTime required for
    certain metrics that are calculated per minute.

    Metrics calculated:
    - [queryRate] number of queries issued per minute (H)
    - [AvgQueryLengthWords] average length of queries issued in words (H)
    - [AvgQueryLengthChars] average length of queries issued in characters
    - [noOfResultsClicked] number of results clicked
    - [DeepestRankVisitedResults] deepest rank of search results visited (H)
    - [AvgRankVisitedResults] average rank of search results visited
    - [serpsVisited] number of SERPs visited
    - dwell time on SERPs per minute (H)
    - actual time used ??

    :param submission: prolific ID of the participant
    :param submissionTime: Time used to complete submission
    :param submissionLogs: the logs of one participant
    :return:
    """
    pagefocusLogs, queryserpLogs, clickLogs = filterLogs(submissionLogs)
    submissionMetrics = {}

    print("***********************************************")

    # Calculate query/serp metrics
    queries, serps = processQueryserpLogs(queryserpLogs)
    submissionMetrics['queryRate'] = len(queries) / (submissionTime / 60)
    submissionMetrics['AvgQueryLengthWords'] = sum(len(query.split()) for query in queries) / len(queries)
    submissionMetrics['AvgQueryLengthChars'] = sum(len(query) for query in queries) / len(queries)
    submissionMetrics['serpsVisited'] = len(serps)

    # Calulate result click metrics
    ranks = extractResultRanksLogs(clickLogs)
    submissionMetrics['noOfResultsClicked'] = len(ranks)
    submissionMetrics['DeepestRankVisitedResults'] =max(ranks)
    submissionMetrics['AvgRankVisitedResults'] = sum(rank for rank in ranks) / len(ranks)

    # Calculate dwell time
    pagefocusInfo = extractPagefocusInformation(pagefocusLogs)

    print(submissionMetrics)


def filterLogs(submissionLogs):
    """
    Filters the JSON logs in the parameter per category:
    pagefocus, query/serp and clicks

    :param submissionLogs: unfiltered JSON logs per participant
    :return: Logs filtered in terms of pagefocus, query/serp and clicks
    """
    pagefocusLogs = []
    queryserpLogs = []
    clickLogs = []

    for submissionLog in submissionLogs:
        if (submissionLog['eventDetails']['type'] == "URLChange"):
            queryserpLogs.append(submissionLog)
        elif (submissionLog['eventDetails']['type'] == 'click' or
              submissionLog['eventDetails']['type'] == 'auxclick'):
            clickLogs.append(submissionLog)
        elif (submissionLog['eventDetails']['type'] == "viewportFocusChange" or
              submissionLog['eventDetails']['type'] == "started" or
              submissionLog['eventDetails']['type'] == "stopped"):
            # Also include start/stop logs in case participant started without focus/endedn without focus.
            pagefocusLogs.append(submissionLog)

    return pagefocusLogs, queryserpLogs, clickLogs


def processQueryserpLogs(queryserpLogs):
    """
    Filter out all the queries and SERP changes. Done in
    this way since are incoorperated in one type of log.

    :param queryserpLogs: the logs containing the queries and serp
    :return: list of the queries issued, list of the serps visited
    """
    queries = []
    serps = []

    for log in queryserpLogs:
        # parse query and serp number
        queryserp_newURL = re.search('^https?:[\/]{2}[0-9.\/a-z-]+\?#([0-9]+)-(.*)$', log['eventDetails']['newURL'])
        queryserp_previousURL = re.search('^https?:[\/]{2}[0-9.\/a-z-]+\?#([0-9]+)-(.*)$', log['eventDetails']['previousURL'])
        # Look at the previous and new query/serp to identify cases below
        if queryserp_newURL and queryserp_previousURL:
            if queryserp_newURL.group(2) == queryserp_previousURL.group(2):
                # Case where query stayed the same and serp number changed
                serps.append(int(queryserp_newURL.group(1)))
            else:
                # Case where query differed, thus new query issued
                serps.append(1)
                queries.append(unquote(unquote(queryserp_newURL.group(2))))
        else:
            # Case without previous query, thus new query issued (from main)
            serps.append(1)
            queries.append(unquote(unquote(queryserp_newURL.group(2))))

    return queries, serps


def extractResultRanksLogs(clickLogs):
    """
    Extract the rank of each clicked result and return in a list.

    :param clickLogs: the clicklogs to extract the ranks from
    :return: the extracted ranks in a list
    """
    return [int(log['metadata'][0]['value']) for log in clickLogs]


def extractPagefocusInformation(pagefocusLogs):
    # CONTINUEEEEEEEEEEE HEREEE
    for log in pagefocusLogs:
        print(log)

# TODO: Add time taken for submission from other source! Using stub of 300 s now.
if __name__ == '__main__':
    logs = importLogs("/home/mike/Downloads/testlogs.log")
    logsPerSubmission = groupLogsPerSubmission(logs)
    for (submission, submissionLogs) in logsPerSubmission.items():
        calculateMetricsPerSubmission(submission, 300, submissionLogs)

