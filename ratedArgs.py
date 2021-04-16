import re


def processRatings(file):
    """
    Read the rated arguments from the CSV and sort them by prolificId and
    by metrics (TDepth, DQual, DInterp)

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
                    ratingsPerSubmission[regexRes.group(1)] = {"TDepth": [], "DQual": [], "DIntrp": []}
                ratingsPerSubmission[regexRes.group(1)]['TDepth'].append(int(regexRes.group(2)))
                ratingsPerSubmission[regexRes.group(1)]['DQual'].append(int(regexRes.group(3)))
                ratingsPerSubmission[regexRes.group(1)]['DIntrp'].append(int(regexRes.group(4)))

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
    file.write("prolificId,avgTDepth,avgDQual,avgDIntrp\n")
    for (prolificId, pRatings) in ratings.items():
        file.write(str(prolificId) + "," + str(avg(pRatings['TDepth'])) + "," + str(avg(pRatings['DQual'])) + "," + str(avg(pRatings['DIntrp'])) + "\n")
    file.close()


def avg(list):
    """
    Calculate the average of a list of ints.

    :param list: list to calculate average of
    :return: average of list
    """
    return sum(list) / len(list)


if __name__ == '__main__':
    processedRatings = processRatings("/home/mike/git/bbt-analysis/data/in/argumentsRated.csv")
    writeAvgRatingsToCSV("/home/mike/git/bbt-analysis/data/out/argumentsAvgRatings.csv", processedRatings)
    print(processedRatings)
