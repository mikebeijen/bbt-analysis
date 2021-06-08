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
    write the time constraint to a CSV for data analysis

    :param file: file to write time statics to
    :param argsSubmissions: The arguments grouped by
                            participant in JSON
    :return: None
    """
    file = open(file, "w")
    file.write("prolificId,timeConstraint\n")
    for s in argsSubmissions:
        if s['timeConstraint'] - s['timeUsed'] < -5:
            # Print a warning if the arguments were submitted more than 5 seconds after the time was up as this could indicate a connection issue.
            print('Participant ' + str(s['_id']) + '\'s arguments submission was not made within 5 seconds after time was up.')
        file.write(s['_id'] + "," + str(s['timeConstraint']) + "\n")

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
            # Replace comma with semicolons and enters with three underscores to prevent corrupting the CSV file
            arg_escaped = arg.replace(',', ';').replace('\n', '___')
            file.write(s['_id'] + ",,,," + arg_escaped + "\n")

    file.close()


if __name__ == '__main__':
    argsSubmissions = importArgs("/home/mike/git/bbt-analysis/data/in/args.json")
    # Calculate time used and write the time statistics to a CSV file for data analysis
    writeTimeStatsAndNoOfArgsToCSV("/home/mike/git/bbt-analysis/data/out/submissionTimesAndNoOfArgs.csv", argsSubmissions)
    # Write arguments to a CSV file with one line per argument for task performance judgements
    writeArgumentsIndividuallyToCSV("/home/mike/git/bbt-analysis/data/out/argumentsToRate.csv", argsSubmissions)
