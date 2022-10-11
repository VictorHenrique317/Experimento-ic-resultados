import matplotlib

# matplotlib.use('agg')
import matplotlib.pyplot as plt
import json
import re
import matplotlib.ticker
from matplotlib import rcParams
import enum
import os


class Attribute(enum.Enum):
    PATTERN_NUMBER = "Nb of patterns"
    RUN_TIME = "Run time"
    MEMORY = "Memory (mb)"
    QUALITY = "Quality"
    TRUNCATED_QUALITY = "Truncated quality"
    RSS_EVOLUTION = "RSS Evolution"


def readPlottingDataFile(path):
    x = []
    y = []
    with open(path, "r") as file:
        json_object = json.load(file)
        x = json_object['x']
        y = json_object['y']

    return x, y


def filterByAttribute(file_names, attribute: Attribute):
    attribute = attribute.value.lower().replace(" ", "")
    return [filename for filename in file_names if attribute in filename]


def listPlottingDataFiles():
    return os.listdir(base_folder)


def translateLabel(algorithm):
    if algorithm == "co16":
        return "16 correct observations"

    if algorithm == "co8":
        return "8 correct observations"

    if algorithm == "co4":
        return "4 correct observations"

    if algorithm == "co2":
        return "2 correct observations"

    if algorithm == "co1":
        return "1 correct observation"

    if algorithm == "fuzzy#getf":
        return "GETF"

    if algorithm == "fuzzy#cancer":
        return "Cancer"

    if algorithm == "fuzzy#nclusterbox":
        return "Slice-input | NclusterBox"

    if algorithm == "fuzzy#slownclusterbox" and dimension == 3:
        return "TriclusterBox"

    if algorithm == "fuzzy#tubeinputnclusterbox" and dimension == 3:
        return "NclusterBox"

    if algorithm == "fuzzy#tubeinputslownclusterbox" and dimension == 3:
        return "NclusterBox minus Sect. 5.1"

    if algorithm == "fuzzy#slownclusterbox" and dimension == 2:
        return "BiclusterBox"

    if algorithm == "fuzzy#tubeinputslownclusterbox" and dimension == 2:
        return "NclusterBox minus Sect. 5.1"

    raise ValueError(f"No label for {algorithm}")


def translateColor(algorithm):
    if algorithm == "co16":
        return "navy"

    if algorithm == "co8":
        return "slateblue"

    if algorithm == "co4":
        return "purple"

    if algorithm == "co2":
        return "magenta"

    if algorithm == "co1":
        return "magenta"

    if algorithm == "fuzzy#getf":
        return "green"

    if algorithm == "fuzzy#cancer":
        return "fuchsia"

    if algorithm == "fuzzy#nclusterbox":
        return "red"

    if algorithm == "fuzzy#slownclusterbox":
        return "orangered"

    if algorithm == "fuzzy#tubeinputnclusterbox":
        return "blue"

    if algorithm == "fuzzy#tubeinputslownclusterbox":
        return "deepskyblue"

    raise ValueError(f"No color for {algorithm}")


def makeGraph(attribute: Attribute, figure_width, figure_height, save=False):
    # axis = plt.gca()
    fig, axis = plt.subplots()
    fig = plt.figure(figsize=(figure_width, figure_height))
    pattern = ".*-.*-.*-(.*)-(co\d*)*"
    # fontsize = 13
    fontsize = 20
    grid_fontsize = fontsize
    legend_fontsize = 22
    labelpad = 32
    plotting_data_files = filterByAttribute(listPlottingDataFiles(), attribute)
    axis = plt.gca()
    title = ""
    str_formatter = ""
    y_str_formatter = ""
    order = []

    for plotting_data_file in plotting_data_files:
        match = re.findall(pattern, plotting_data_file)
        if len(match) == 0:
            continue

        algorithm = match[0][0]
        tensor_type = algorithm.split("#")[0]
        if attribute == Attribute.RSS_EVOLUTION:
            # str_formatter = '{x:.2f}'
            grid_fontsize = fontsize-6
            if "tubeinputnclusterbox" not in algorithm:
                continue

            observations = match[0][1]
            color = translateColor(algorithm)
            order = []

            title = "RSS evolution across multiple noise levels"
            if observations != "co16":
                continue

            str_formatter = '{x: .0f}'
            y_str_formatter = '{x: .0f}'

            x, y = readPlottingDataFile(f"{base_folder}/{plotting_data_file}")

            x = x[:20]
            y = y[:20]
            x_ticks = [tick for tick in range(0, max(x) + 1, 1)]
            x_ticks[0] = 1

            # plt.plot(x, y, label=translateLabel(observations), color=color)
            plt.plot(x, y, color=color)
            plt.scatter(x, y, color=color)
            plt.yscale("linear")
            plt.xscale("linear")
            plt.ylabel("RSS", fontsize=fontsize, labelpad=labelpad)
            plt.xlabel("number of patterns selected by truncation of Alg. 5's output", fontsize=fontsize, labelpad=labelpad)
            axis.set_xticks(x_ticks)

        else:  # other graphs
            str_formatter = '{x: .0f}'
            y_str_formatter = '{x: .0f}'

            if attribute == Attribute.PATTERN_NUMBER:
                algorithm_runtime_legend_order = [4, 0, 1, 2, 3]
                order = algorithm_runtime_legend_order
                y_str_formatter = '{x: .0f}'
                title = "Number of patterns selected by truncation of Alg. 5's output"
                plt.ylabel("number of patterns selected by truncation of Alg. 5's output", fontsize=fontsize, labelpad=labelpad)
                plt.yscale("log")

            elif attribute == Attribute.QUALITY:
                y_str_formatter = '{x: .2f}'
                if algorithm == "fuzzy#nclusterbox":
                    continue

                if algorithm == "fuzzy#tubeinputslownclusterbox":
                    continue

                algorithm_quality_legend_order = [0,1,2]
                order = algorithm_quality_legend_order

                title = "Quality"
                grid_fontsize = fontsize - 4
                axis.set_ylim((-0.008, 1.008))
                plt.ylabel("quality", fontsize=fontsize, labelpad=labelpad)

            elif attribute == Attribute.RUN_TIME:
                if algorithm == "fuzzy#nclusterbox":
                    continue
                # axis.set_ylim(0, 45)
                axis.set_ylim(0, 45)
                algorithm_runtime_legend_order = [3, 0, 1, 2]
                order = algorithm_runtime_legend_order
                y_str_formatter = '{x: .2f}'
                grid_fontsize = fontsize - 4
                title = "Run time (seconds)"
                plt.ylabel("run time (seconds)", fontsize=fontsize, labelpad=labelpad)
                plt.yscale("linear")

            color = translateColor(algorithm)
            print("=========================")
            print(f"{algorithm}")
            print(f"{color}")
            # order = ALGORITHM_LEGEND_ORDER

            x, y = readPlottingDataFile(f"{base_folder}/{plotting_data_file}")
            plt.xlim(max(x), min(x))
            plt.plot(x, y, label=translateLabel(algorithm), color=color)
            plt.scatter(x, y, color=color)
            # plt.yscale("linear")
            plt.xscale("log", basex=2)
            plt.xlabel("number of correct observations", fontsize=fontsize, labelpad=labelpad)

    print(order)
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order], fontsize=legend_fontsize)
    # plt.legend()
    axis.tick_params(labelsize=grid_fontsize)

    plt.grid()
    # plt.title(title, y=1.05, fontsize=fontsize)
    # axis.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    axis.get_xaxis().set_major_formatter(matplotlib.ticker.StrMethodFormatter(f'{str_formatter}'))
    axis.get_yaxis().set_major_formatter(matplotlib.ticker.StrMethodFormatter(f'{y_str_formatter}'))

    # rcParams['axes.titlepad'] = 32

    if save:
        plt.savefig(f"{base_folder}/saves/{title.lower().replace(' ', '-')}")
        plt.close(fig)
    else:
        plt.show()


dimension = 3
experiment_type = "synthetic"


# ALGORITHM_RUNTIME_LEGEND_ORDER = [4, 0, 1, 2, 3] # run time 3D
ALGORITHM_QUALITY_LEGEND_ORDER = [4, 0, 1, 2, 3] # quality 3D
# ALGORITHM_LEGEND_ORDER = []
OBSERVATIONS_LEGEND_ORDER = [3, 1, 2, 0, 4]

base_folder = f"{experiment_type}/{dimension}d"
# makeGraph(Attribute.RSS_EVOLUTION, "observations", scale='linear')
makeGraph(Attribute.RUN_TIME, 14, 10, save=False)
