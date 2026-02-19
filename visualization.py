import matplotlib.pyplot as plt


def graph_total_population(alive_over_time):
    """Graph total population over time using matplotlib

    Args:
        param1: list of tuples of time and alive organisms at that time

    Returns:
        None, displays graph of total population over time
    """

    time, total_population = zip(*alive_over_time)

    plt.figure()
    plt.plot(time, total_population)

    # Label axes and title
    plt.xlabel("Time")
    plt.ylabel("Total Population")
    plt.title("Total Population vs Time")

    # Add grid for readability
    plt.grid(True)

    # Show the graph
    plt.show()
