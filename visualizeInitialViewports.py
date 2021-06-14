import matplotlib.pyplot as plt
import re

def importSizes(path):
    """
    Import the initial viewport sizes from the CSV file.

    :param path: Path to the CSV file.
    :return: Array of initial sizes
    """
    initialSizes = []

    with open(path) as file:
        for line in file:
            # Use regex to extract Prolific ID, width, height
            regexRes = re.search("^([a-z0-9]{24}),([0-9]+),([0-9]+)$", line)
            if regexRes:
                initialSizes.append((int(regexRes.group(2)), int(regexRes.group(3))))

    return initialSizes


if __name__ == '__main__':
    sizes = importSizes("/home/mike/git/bbt-analysis/data/out/initialViewports.csv")

    # Plot all initial sizes.
    xcors = [cor[0] for cor in sizes]
    ycors = [cor[1] for cor in sizes]
    plt.scatter(xcors, ycors)
    plt.show()