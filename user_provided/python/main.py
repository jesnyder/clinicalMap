
from list_trials import list_trials
from query_openmaps import query_openmaps
from assign_groups import assign_groups
from write_geojson import write_geojson
from year_counts import year_counts

def main():
    """
    Objective
    Map clinical trials
    """

    tasks = []
    #tasks.append('openmaps')

    # list trials
    if 0 in tasks: list_trials()

    # assign groups
    if 1 in tasks: assign_groups()

    # geolocate locations
    if 'openmaps' in tasks: query_openmaps()

    # write geojson
    if 3 in tasks: write_geojson()

    # tally totals
    if 4 in tasks: year_counts()


if __name__ == "__main__":
    main()
