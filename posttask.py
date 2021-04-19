import json


def importPosttasks(file):
    """
    Import the raw JSON posttask questionnaires as a
    list of JSON object.

    :param file: file containing the raw JSON to import
    :return: imported args as JSON objects
    """
    posttasks_json = []
    with open(file) as file:
        for line in file:
            posttasks_json.append(json.loads(line))
    return posttasks_json


def processSubmission(posttaskSubmission):
    """
    Calculate the ATI score and the sub and total scores of the
    User Experience Scale. Also check if attention check was passed.

    :param posttaskSubmission: the posttask questionnaire in JSON
    :return: calculated metrics in JSON format.
    """
    posttaskMetrics = { 'prolificID': posttaskSubmission['_id'] }

    # Calculate ATI score
    posttaskMetrics['ati'] = sum([posttaskSubmission['ati' + str(i)] for i in range(1, 10)]) / 9

    # Calculate UES subscores and final scores
    posttaskMetrics['uesRws'] = sum([posttaskSubmission['rws' + str(i)] for i in range(1, 4)]) / 3
    posttaskMetrics['uesAes'] = sum([posttaskSubmission['aes' + str(i)] for i in range(1, 4)]) / 3
    posttaskMetrics['uesPus'] = sum([posttaskSubmission['pus' + str(i)] for i in range(1, 4)]) / 3
    posttaskMetrics['uesFas'] = sum([posttaskSubmission['fas' + str(i)] for i in range(1, 4)]) / 3
    posttaskMetrics['uesTotal'] = (posttaskMetrics['uesRws'] + posttaskMetrics['uesAes'] + posttaskMetrics['uesPus'] + posttaskMetrics['uesFas']) / 4

    # Print message if attention check was failed
    if not posttaskSubmission['attn'] == 2:
        print("[WARNING] Participant " + posttaskSubmission['_id'] + " failed the attention check!")

    return posttaskMetrics


def writeToCSV(out_file, processedSubmissions):
    """
    Write the calculated metrics to a CSV file.

    :param out_file: the file to write to.
    :param processedSubmissions: the results to write
                                    to the file.
    :return: None
    """
    file = open(out_file, "w")
    file.write("prolificID,ati,uesRws,uesAes,uesPus,uesFas,uesTotal\n")
    for s in processedSubmissions:
        file.write(s['prolificID'] + "," + str(s['ati']) + "," + str(s['uesRws']) + "," + str(s['uesAes']) + "," + str(s['uesPus']) + "," + str(s['uesFas']) + "," + str(s['uesTotal']) + "\n")
    file.close()

if __name__ == '__main__':
    # Load raw posttask questionnaires from file
    posttaskSubmissions = importPosttasks("/home/mike/git/bbt-analysis/data/in/posttask.json")

    # Calculate the necessary metrics
    processedSubmissions = [processSubmission(s) for s in posttaskSubmissions]

    # Write the required metrics to a CSV file to be able to import later for statistical analysis.
    writeToCSV("/home/mike/git/bbt-analysis/data/out/posttask.csv", processedSubmissions)
