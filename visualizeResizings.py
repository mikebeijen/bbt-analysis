import matplotlib.pyplot as plt
import re

def plotResizings(resizings, color):
    """
    Plot arrows representing the resizing events.

    :param resizings: Array with the resizing events of one participant
    :param color: Color of the resizing event.
    :return: Nothing.
    """
    last = None
    for (x, y) in resizings:
        if last is not None:
            plt.arrow(last[0], last[1], x - last[0], y - last[1], head_width=25, length_includes_head=True, color=color)
            last = (x, y)
        else:
            last = (x, y)


def importResizings(path):
    """
    Import the resizing events, group by participant.

    :param path: Path to the file containing the resizing event.
    :return: Resizing events grouped by participant.
    """
    resizingsPerParticipants = {}

    with open(path) as file:
        for line in file:
            # Use regex to extract Prolific ID, width, height
            regexRes = re.search("^([a-z0-9]{24}),([0-9]+),([0-9]+)$", line)
            if regexRes:
                if not regexRes.group(1) in resizingsPerParticipants:
                    resizingsPerParticipants[regexRes.group(1)] = [(int(regexRes.group(2)), int(regexRes.group(3)))]
                else:
                    resizingsPerParticipants[regexRes.group(1)].append((int(regexRes.group(2)), int(regexRes.group(3))))

    return resizingsPerParticipants

if __name__ == '__main__':

    allResizings = importResizings("/data/out/resizings.csv")
    print(len(allResizings))

    # create a color map to be able to distinguish arrows
    colorMap = plt.cm.get_cmap('hsv', len(allResizings))

    # Plot all resizing events
    for i, resizing in enumerate(allResizings):
        plotResizings(allResizings[resizing], colorMap(i))

    plt.show()
