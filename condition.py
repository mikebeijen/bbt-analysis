import json


def processConditions(file, outfile):
    """
    Convert the raw JSON conditions to a CSV file.

    :param file: file containing the raw conditions to convert
    :param outfile: file to write output too
    :return: None
    """
    with open(file, "r") as conditions_file:
        with open(outfile, "w") as csv_file:
            csv_file.write("prolificID,condition\n")
            for line in conditions_file:
                pretask = json.loads(line)
                csv_file.write(pretask['_id'] + "," + str(pretask['condition']) + "\n")
        csv_file.close()
    conditions_file.close()


if __name__ == '__main__':
    processConditions("/home/mike/git/bbt-analysis/data/in/condition.json", "/home/mike/git/bbt-analysis/data/out/condition.csv")

