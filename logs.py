import json
from urllib.parse import unquote
import re
import datetime


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
        if (prolificid not in submissionsGrouped) and (log['eventType'] == "statusEvent" and log['eventDetails']['type'] == "started"):
            submissionsGrouped.update({prolificid: [log]})
        elif prolificid in submissionsGrouped:
            submissionsGrouped[prolificid].append(log)
    submissionsGrouped.pop(None, None)
    return submissionsGrouped


def calculateMetricsPerSubmission(submission, submissionTime, submissionLogs):
    """
    calculate search behavior metrics from the logs
    of one participant. SubmissionTime required for
    certain metrics that are calculated per minute.

    Metrics calculated:
    - [queriesIssued] number of queries issued in total
    - [queryRate] number of queries issued per minute (H)
    - [avgQueryLengthWords] average length of queries issued in words (H)
    - [avgQueryLengthChars] average length of queries issued in characters
    - [noOfResultsClicked] number of results clicked
    - [deepestRankVisitedResults] deepest rank of search results visited (H)
    - [avgRankVisitedResults] average rank of search results visited
    - [serpsVisited] number of SERPs visited
    - [dwellTimePerMinute] dwell time on SERPs per minute (H)

    :param submission: prolific ID of the participant
    :param submissionTime: Time used to complete submission
    :param submissionLogs: the logs of one participant
    :return:
    """
    pagefocusLogs, queryserpLogs, clickLogs, startLogs, stopLogs = filterLogs(submissionLogs)
    submissionMetrics = {"prolificId": submission}

    print("***********************************************")

    # Calculate query/serp metrics
    queries, serps = processQueryserpLogs(queryserpLogs)
    print(queries)
    print(serps)
    submissionMetrics['queriesIssued'] = len(queries)
    submissionMetrics['queryRate'] = len(queries) / (submissionTime / 60)
    submissionMetrics['avgQueryLengthWords'] = 0 if len(queries) == 0 else sum(len(query.split()) for query in queries) / len(queries)
    submissionMetrics['avgQueryLengthChars'] = 0 if len(queries) == 0 else sum(len(query) for query in queries) / len(queries)
    submissionMetrics['serpsVisited'] = len(serps)

    # Calulate result click metrics
    # Set the last two to 0 if no results were clicked
    ranks = extractResultRanksLogs(clickLogs)
    submissionMetrics['noOfResultsClicked'] = len(ranks)
    submissionMetrics['deepestRankVisitedResults'] = 0 if len(ranks) == 0 else max(ranks)
    submissionMetrics['avgRankVisitedResults'] = 0 if len(ranks) == 0 else sum(rank for rank in ranks) / len(ranks)

    # Calculate dwell time
    pagefocusIntervals = extractPagefocusIntervals(pagefocusLogs, startLogs, stopLogs)
    submissionMetrics['dwellTimePerMinute'] = sum((endTime - startTime) for (startTime, endTime) in pagefocusIntervals) / 1000 / (submissionTime / 60)

    print(submissionMetrics)
    return submissionMetrics


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
    startLogs = []
    stopLogs = []

    for submissionLog in submissionLogs:
        if (submissionLog['eventDetails']['type'] == "URLChange"):
            queryserpLogs.append(submissionLog)
        elif (submissionLog['eventDetails']['type'] == 'click' or
              submissionLog['eventDetails']['type'] == 'auxclick' or
              submissionLog['eventDetails']['type'] == 'mouseClick'):
            clickLogs.append(submissionLog)
        elif (submissionLog['eventDetails']['type'] == "viewportFocusChange"):
            pagefocusLogs.append(submissionLog)
        # Also include start/stop logs in case participant started without focus/ended without focus.
        elif (submissionLog['eventDetails']['type'] == "started"):
            startLogs.append(submissionLog)
        elif (submissionLog['eventDetails']['type'] == "stopped"):
            stopLogs.append(submissionLog)

    return pagefocusLogs, queryserpLogs, clickLogs, startLogs, stopLogs


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
        elif not queryserp_newURL:
            # Case where no new query was issued. Can happen on refresh or return to main landing page.
            # Pass since its no serp visit or query issued
            pass
        elif not queryserp_previousURL and queryserp_newURL:
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


def extractPagefocusIntervals(pagefocusLogs, startLogs, stopLogs):
    """
    Calculate the intervals in which the pagefocus was on the SERP.

    :param pagefocusLogs: logs of pagefocusEvent
    :param startLogs: logs of LogUI being started
    :param stopLogs: logs of LogUI being stopped
    :return: list of focus intervals in millis
    """
    # include start/stop times if the user started with focus/ended without focus.
    startLogTime = int(datetime.datetime.strptime(startLogs[0]['timestamps']['eventTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000)
    stopLogTime = int(datetime.datetime.strptime(stopLogs[-1]['timestamps']['eventTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000)

    lastTimestamp = startLogTime
    lastFocus = False
    focusIntervals = []

    for log in pagefocusLogs:
        timestamp = int(datetime.datetime.strptime(log['timestamps']['eventTimestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000)
        hasFocus = log['eventDetails']['hasFocus']

        # Add a focus interval if we went from true to false.
        if not hasFocus:
            focusIntervals.append((lastTimestamp, timestamp))

        lastTimestamp = timestamp
        lastFocus = hasFocus

    # Close off last focus interval with stoptime if unfocused when time was over
    if lastFocus:
        focusIntervals.append((lastTimestamp, stopLogTime))

    return focusIntervals


def writeToCSV(out_file, submissionMetrics):
    file = open(out_file, "w")
    file.write("prolificId,queriesIssued,queryRate,avgQueryLengthWords,avgQueryLengthChars,serpsVisited,noOfResultsClicked,deepestRankVisitedResults,avgRankVisitedResults,dwellTimePerMinute\n")
    for s in submissionMetrics:
        file.write(s['prolificId'] + "," + str(s['queriesIssued']) + "," + str(s['queryRate']) + "," + str(s['avgQueryLengthWords']) + "," + str(s['avgQueryLengthChars']) + "," + str(s['serpsVisited']) + "," +
                   str(s['noOfResultsClicked']) + "," + str(s['deepestRankVisitedResults']) + "," + str(s['avgRankVisitedResults']) + "," + str(s['dwellTimePerMinute']) + "\n")
    file.close()


def getSubmissionTimes(file):
    submissionTimes = {}
    with open(file) as submissions_file:
        next(submissions_file)
        for s in submissions_file:
            regexRes = re.search("^([a-z0-9]{24}),([0-9]+),[0-9]+,[0-9]+$", s)
            if regexRes:
                submissionTimes[regexRes.group(1)] = int(regexRes.group(2))

    return submissionTimes


if __name__ == '__main__':
    logs = importLogs("/home/mike/git/bbt-analysis/data/in/logs-list.log")
    logsPerSubmission = groupLogsPerSubmission(logs)
    submissionTimes = getSubmissionTimes("/home/mike/git/bbt-analysis/data/out/submissionTimesAndNoOfArgs.csv")
    submissionMetrics = []
    for (submission, submissionLogs) in logsPerSubmission.items():
        if submission in submissionTimes:
            submissionMetrics.append(calculateMetricsPerSubmission(submission, submissionTimes[submission], submissionLogs))
    writeToCSV("/home/mike/git/bbt-analysis/data/out/submissionMetrics.csv", submissionMetrics)


