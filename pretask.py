import json


def importPretasks(file, outfile):
    """
    Convert the raw JSON pretask questionnaires to a CSV file.
    Output warning if an attention check was failed.

    :param file: file containing the raw pretasks to convert
    :return: None
    """
    with open(file, "r") as pretasks_file:
        with open(outfile, "w") as csv_file:
            csv_file.write("prolificID,gender,age,education,wse,priorknowl,interest,taskdef\n")
            for line in pretasks_file:
                pretask = json.loads(line)
                print(line)
                if not pretask['attn'] == 1:
                    print("[WARNING] Participant " + pretask['_id'] + " failed the attention check!")
                csv_file.write(pretask['_id'] + "," + str(pretask['gender']) + "," + str(pretask['age']) + "," + str(pretask['education']) + "," + str(pretask['wse']) + "," + str(pretask['priorknowl']) + "," + str(pretask['interest']) + "," + str(pretask['taskdef']) + "\n")
        csv_file.close()
    pretasks_file.close()


if __name__ == '__main__':
    pretaskSubmissions = importPretasks("/home/mike/git/bbt-analysis/data/in/pretask.json", "/home/mike/git/bbt-analysis/data/out/pretasks.csv")

