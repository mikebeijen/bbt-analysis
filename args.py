import json


def importArgs(file):
    """
    Import the raw JSON arguments as a dictionary.

    :param file: file containing the raw arguments to import
    :return: imported args as JSON
    """
    args_json = []
    with open(file) as args_file:
        for line in args_file:
            args_json.append(json.loads(line))

    return args_json


def writeTimeStatsAndNoOfArgsToCSV(file, argsSubmissions):
    """
    Calculate time used to complete the submission and
    write the time statistics to a CSV for data analysis

    :param file: file to write time statics to
    :param argsSubmissions: The arguments grouped by
                            participant in JSON
    :return: None
    """
    file = open(file, "w")
    file.write("prolificId,timeRemaining,timeConstraint,timeUsed,noOfArgsSubmitted\n")
    for s in argsSubmissions:
        if s['timeRemaining'] < 0:
            file.write(s['_id'] + "," + str(s['timeRemaining']) + "," + str(s['timeConstraint']) + "," + str(s['timeConstraint']) + "," + str(len(s['args'])) + "\n")
        else:
            timeUsed = s['timeConstraint'] - s['timeRemaining']
            file.write(s['_id'] + "," + str(s['timeRemaining']) + "," + str(s['timeConstraint']) + "," + str(timeUsed) + "," + str(len(s['args'])) + "\n")

    file.close()


def writeArgumentsIndividuallyToCSV(file, argsSubmissions):
    """
    Write arguments to a CSV file with one line per argument for task performance judgements

    :param file: file to write time statics to
    :param argsSubmissions: The arguments grouped by
                            participant in JSON
    :return: None
    """
    file = open(file, "w")
    file.write("prolificId,TDepth,DQual,DIntrp,Argument\n")
    for s in argsSubmissions:
        for arg in s['args']:
            file.write(s['_id'] + ",,,," + arg + "\n")

    file.close()


if __name__ == '__main__':
    argsSubmissions = importArgs("/home/mike/git/bbt-analysis/data/in/args.json")
    # Calculate time used and write the time statistics to a CSV file for data analysis
    writeTimeStatsAndNoOfArgsToCSV("/home/mike/git/bbt-analysis/data/out/submissionTimesAndNoOfArgs.csv", argsSubmissions)
    # Write arguments to a CSV file with one line per argument for task performance judgements
    writeArgumentsIndividuallyToCSV("/home/mike/git/bbt-analysis/data/out/argumentsToRate.csv", argsSubmissions)
