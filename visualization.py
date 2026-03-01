import matplotlib.pyplot as plt
from numpy import nan


def graph_total_population(alive_over_time):
    """Graph total population over time using matplotlib

    Args:
        param1: list of tuples of time and alive organisms at that time

    Returns:
        None, displays graph of total population over time
    """

    # Get independent times and total population lists from alive_over_time
    time, total_population = zip(*alive_over_time)

    plt.figure(num="Total Population Per Iteration")
    plt.plot(time, total_population)

    # Set Y axis to integer tick marks only.
    plt.locator_params(axis='y', integer=True)

    # Label axes and title
    plt.xlabel("Iteration Number")
    plt.ylabel("Total Population")
    plt.title("Total Population per Iteration")

    # Add grid for readability
    plt.grid(True)

    # Show the graph
    plt.show()


def graph_color_population(color_over_time):
    """Graph color population over time using matplotlib

    Args:
        param1: list of tuples of time and dictionary of colors at that time

    Returns:
        None, displays graph of total color population over time
    """
    times = []
    all_color_dict = {}

    # Build a dictionary of all colors and a list of times
    for time, color_dict in color_over_time:
        times.append(time)
        for color in color_dict:
            if color not in all_color_dict:
                all_color_dict[color] = []

    # populate the all_color_dict with the counts for each color at each time
    for time, color_dict in color_over_time:
        for color, counts in all_color_dict.items():
            if color in color_dict:
                all_color_dict[color].append(color_dict[color])
            else:
                all_color_dict[color].append(0)

    plt.figure(num="Genome Color Population Per Iteration")
    for color, counts in all_color_dict.items():
        plot_color = tuple([x/255 for x in color])

        # Don't plot zero counts unless it's the first zero or last zero
        for index, value in enumerate(counts):
            if index == 0:
                prev_value = 0
            else:
                prev_value = counts[index - 1]

            if index + 1 <= len(counts) - 1:
                next_value = counts[index + 1]
            else:
                next_value = 0

            if value == 0 and prev_value == 0 and next_value == 0:
                counts[index] = nan

        plt.plot(times, counts, label=color, color=plot_color)

    # Set Y axis to integer tick marks only.
    plt.locator_params(axis='y', integer=True)

    # Label axes and title
    plt.xlabel("Iteration Number")
    plt.ylabel("Population by color")
    plt.title("Genome Color Population per Iteration")

    # Add grid for readability
    plt.grid(True)

    # Show the graph
    plt.show()


def graph_plant_population(plant_over_time):
    """Graph total plant population over time using matplotlib

    Args:
        param1: list of tuples of time and alive plants at that time

    Returns:
        None, displays graph of total plant population over time
    """

    # Get independent times and total population lists from alive_over_time
    time, plant_population = zip(*plant_over_time)

    plt.figure(num="Total Population Per Iteration")
    plt.plot(time, plant_population)

    # Set Y axis to integer tick marks only.
    plt.locator_params(axis='y', integer=True)

    # Label axes and title
    plt.xlabel("Iteration Number")
    plt.ylabel("Total Plant Population")
    plt.title("Total Plant Population per Iteration")

    # Add grid for readability
    plt.grid(True)

    # Show the graph
    plt.show()
