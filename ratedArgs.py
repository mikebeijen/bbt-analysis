import re


def processRatings(file):
    """
    Read the rated arguments from the CSV and sort them by prolificId and
    by metrics (TDepth, DQual, DInterp)
    As for T-Depth, each argument should have the number of one of the four
    subtopics it fits with best.


    :param file: the file to read the rated arguments from
    :return: argument ratings for all submissions sorted by prolificId and metric
    """
    ratingsPerSubmission = {}
    with open(file) as ratings_file:
        next(ratings_file)
        for line in ratings_file:
            regexRes = re.search("^([a-z0-9]{24}),([0-4]),([0-4]),([0-4]),(.*)$", line)
            if regexRes:
                if not regexRes.group(1) in ratingsPerSubmission:
                    ratingsPerSubmission[regexRes.group(1)] = {"DQual": [], "DIntrp": [], "TDepth-subtopic1": 0,
                                                               "TDepth-subtopic2": 0, "TDepth-subtopic3": 0, "TDepth-subtopic4": 0}
                if regexRes.group(2) != '0':
                    ratingsPerSubmission[regexRes.group(1)]['TDepth-subtopic' + regexRes.group(2)] += 1
                ratingsPerSubmission[regexRes.group(1)]['DQual'].append(int(regexRes.group(3)))
                ratingsPerSubmission[regexRes.group(1)]['DIntrp'].append(int(regexRes.group(4)))

    # Calculate T-Depth
    for (submission, ratings) in ratingsPerSubmission.items():
        ratingsPerSubmission[submission]['TDepth'] = avg([min(3, ratings["TDepth-subtopic" + str(i)]) for i in range(1, 5)])

    return ratingsPerSubmission


def writeAvgRatingsToCSV(file, ratings):
    """
    Calculate the average ratings of each metrics of each submission.
    Then, write to CSV file.

    :param file: the CSV file to write the average ratings to.
    :param ratings: the processed ratings.
    :return: None
    """
    file = open(file, "w")
    file.write("prolificId,avgTDepth,avgDQual,avgDIntrp,NoOfArgsSubmitted\n")
    for (prolificId, pRatings) in ratings.items():
        file.write(str(prolificId) + "," + str(pRatings['TDepth']) + "," + str(avg(pRatings['DQual'])) + "," + str(avg(pRatings['DIntrp'])) + "," + str(len(pRatings['DIntrp'])) + "\n")
    file.close()


def avg(list):
    """
    Calculate the average of a list of ints.

    :param list: list to calculate average of
    :return: average of list
    """
    return sum(list) / len(list)


if __name__ == '__main__':
    processedRatings = processRatings("/home/mike/git/bbt-analysis/data/in/allArgsRated.csv")
    writeAvgRatingsToCSV("/home/mike/git/bbt-analysis/data/out/argumentsAvgRatings.csv", processedRatings)
    print(processedRatings)
