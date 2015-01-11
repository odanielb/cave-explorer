#-------------------------------------------------------------------------------
# Name:        map-explorer-driver.py
# Purpose:  To use the Explorer and Location classes to navigate a provided map
#           and collect all the treasure possible.
#
# Author:      odanielb
#
# Acknowledgements: Cleaning file help from :http://stackoverflow.com/questions/10794245/removing-spaces-and-empty-lines-from-a-file-using-python
#-------------------------------------------------------------------------------
import time
import copy
from Explorer import Explorer
from Location import Location


def read_map(file_name):
    """This function opens a file with the name in 'file_name', reads the map it
    contains. Stores each line of the file as strings in a list.
    pre: none, as this function handles IOError for when the file is not there gracefully
    post: Returns a list of strings."""
    map_file_list_of_rows = []
    try:
        open_file = open(file_name, 'r')            #Open the specified file
        for line in open_file:
            cleaned_line = line.strip()
            if 'W' in line:
                cleaned_line = cleaned_line.replace(" ", "")
            map_file_list_of_rows.append(cleaned_line)
        open_file.close()                           #Close the file
    except IOError:
        print("File does not exist! Try again.")    #If it can't find this file.
    return map_file_list_of_rows


def finalize_map(map_list):
    """Makes the tuple of tuples that contain Locations according to a given
    string.
    pre: map_string is a list of strings returned by the function read_map
    post: returns the map as represented as a tuple of tuples containing Locations."""
    dimensions = map_list[0].split()
    map_ = []
    for i in range(int(dimensions[0])):  #For each row
        row = list(map_list[i+1])
        map_.append(row)
    map_tup = _create_locations(map_)
    return map_tup


def initialize_map(file_name):
    """Using the provided file_name, reads from a file and creates a map to be
    used by an Explorer.
    pre: file_name is a string with the valid name of a .txt file (including
    extension).
    post: returns the map as a tuple of tuples (rows, containing locations)"""
    read_file_list = read_map(file_name)
    the_map = finalize_map(read_file_list)
    return the_map


def _create_locations(list_of_lists):
    """From the list of lists (each representing a row), creates a tuple containing
    the tuples of rows, each row containing a Location object rather than the strings
    provided in the list_of_lists.
    pre: list_of_lists is a list of lists, each nested list containing the same
    number of strings (each one character long).
    post: returns a tuple of tuples of Locations."""
    lol = copy.deepcopy(list_of_lists)
    for row, lst in enumerate(lol):
        for col, string in enumerate(lst):
            loc = Location(row,col,string)
            lol[row][col] = loc
        lol[row] = tuple(lst)
    lol = tuple(lol)
    return lol


def find_explorer_location(map):
    """Returns the Location on map that contains the explorer, M.
    pre: map is the map represented as a tuple of tuples of Locations.
    post: Returns the Location containing M."""
    for i, row in enumerate(map):
        for j, loc in enumerate(row):
            if loc.get_contents() == 'M':
                return loc

def main():
    file_name = raw_input("What is the name of the file containing the map? (.txt included)")
    the_map = initialize_map(file_name)                                         #Create the map

    explorer_loc = find_explorer_location(the_map)                              #Find the location of the explorer
    explorer = Explorer(explorer_loc, the_map)                                  #Initialize the explorer
    explorer.add_position_to_diary(explorer_loc.get_pos())                      #Explorer notes where it is in its diary

    is_more = True
    while is_more:                                                              #While the explorer is not at the start OR there are unexplored directions:
        time.sleep(1)                                                                  #Wait two seconds
        explorer.display_map()                                                  #Display the current map
        is_more = explorer.move()                                                       #Try to move a space, is_more = None if it cannot
    print("You've collected "+str(explorer.get_treasure_count())+" treasure!")


if __name__ == '__main__':
    main()
