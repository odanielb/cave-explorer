#-------------------------------------------------------------------------------
# Name:        Explorer.py
# Purpose: To create an Explorer with a map who will be able to adventure through
#          the map and collect treasure.
#
# Author:      odanielb (Bridget O'Daniel)
#
# Acknowledgements: Future print statement from: http://stackoverflow.com/questions/388069/python-graceful-future-feature-future-import
#-------------------------------------------------------------------------------
from __future__ import print_function
from Stack import Stack
from Location import Location

class Explorer (object):

    DIRECTIONS = ['N','E', 'W', 'S']
    DIRECTION_OPP = {'N':'S', 'S':'N', 'E':'W', 'W':'E'}

    def __init__(self, location, explorer_map):
        """Creates a new Explorer."""
        self.name = 'M'
        self.pos = location.get_pos()
        self.treasure = 0
        self.steps_taken = Stack()
        self.position_diary = {}
        self.map = explorer_map


    def get_pos(self):
        """Returns the current position of the Explorer in the format (row, col).
        post: returns a tuple containing two ints."""
        return self.pos


    def get_row(self):
        """Returns the current row of the Explorer.
        post: returns an int."""
        return self.pos[0]


    def get_col(self):
        """Returns the current column of the Explorer.
        post: returns an int."""
        return self.pos[1]


    def get_treasure_count(self):
        """Returns the amount of treasure collected by the Explorer.
        post: returns an int."""
        return self.treasure


    def get_pos_of_location_in_direction(self, direction, position=0):
        """Returns the position of the location one spot in the provided direction,
        from the provided position. If no position is provided, it is assumed to
        be the current position.
        pre: direction must be a string with a letter from the following: 'NEWS'
        position must be a tuple of two ints such that (row, col).
        post: Returns a tuple in the form (row, col.)"""
        if position == 0:
            row, col = self.get_pos()
        else:
            row, col = position
        if direction in 'NEWS':
            if direction == 'N':
                return (row-1, col)
            elif direction == 'E':
                return (row, col+1)
            elif direction == 'W':
                return (row, col-1)
            elif direction == 'S':
                return (row+1, col)

    def set_pos(self, row, col):
        """Sets the position of Explorer to (row, col).
        pre: row and col are ints and (row, col) is a position on the map.
        post: Changes self.pos to (row, col)"""
        self.pos = (row, col)


    def backtrack(self):
        """The Explorer goes back to the last Location it was at. If it can
        backtrack no further, the Explorer has explored everything in the cave."""
        if self.steps_taken.size() > 0:
            direction = self.get_opposite_direction(self.pop_last_direction())  #Pop direction last gone and find its opposite (backtrack = go in opp. direction)
            self._update_explorer_pos(direction)                                #Update the position of Explorer appropriately


    def move(self):
        """The Explorer attempts to move based on the following prerequisites,
        and returns True unless the cave has been fully explored:
            -If there are directions from the current Location that the Explorer
            has not yet been, it will prioritize in this order: (N > E > W > S).
            -If Explorer has been in every possible direction from this Location,
            it backtrack one spot.
            -If Explorer cannot backtrack but has been in every possible direction,
            it has explored the whole cave and None is returned.
        pre: Current position is already in position diary.
        post: Returns True or None."""
        direction = self.decide_where_to_go()                                   #Decides where to go

        if direction not in 'NEWS':
            if direction == 'No':
                return None
            self.backtrack()                                                    #If direction wasn't in 'NEWS', but wasn't 'None', it would be 'Backtrack'

        else:                                                               #If it is a normal direction,
            self.steps_taken.push(direction)                                    #Add the direction gone in on top of the steps_taken stack
            self._update_explorer_pos(direction)                                #Properly moves Explorer and collects treasure if any.

            if self.is_position_in_diary():                                     #If the current (ie, new) position is in the position diary,
                self.update_position_diary()                                        #Update diary to include the direction gone in, for last and current pos
            else:                                                               #If not in diary,
                self.add_position_to_diary()                                        #Add the current position to the position diary
                self.update_position_diary()                                        #Update diary to include the direction gone in, for last and current pos
        return True


    def _update_explorer_pos(self, direction):
        """Using the given direction, changes Explorer's location to the next
        spot in that direction, making the appropriate changes to positions and
        Location contents, including collecting treasure.
        pre: direction is a string of one character in 'NEWS'."""
        old_row, old_col = self.get_pos()                                       #Get row and column of location before moving
        self.map[old_row][old_col].set_contents('.')                            #Set the Location to contain a path rather than the explorer
        new_row, new_col = self.get_pos_of_location_in_direction(direction)     #Get the position to move to
        self.set_pos(new_row, new_col)                                          #Set Explorer's new position

        new_loc = self.map[new_row][new_col]                                    #Variable for the new location
        if new_loc.get_contents() == 'T':                                       #If the new location contains Treasure:
            self.collect_treasure(new_loc)                                          #Collect treasure and display path there using 'X's
 #       else:
 #           self.steps_since_treasure += 1                                          #Keep this value updated

        new_loc.set_contents('M')                                               #Set new Location to contain the explorer


    def collect_treasure(self, location):
        """The Explorer will collect the treasure that is in this Location.
        pre: location is a Location object with the same position as Explorer."""
        self.treasure += 1                                                                          #Add treasure

        temp_stack = Stack()                                                                        #Temporary stack to store popped directions
        row, col = self.get_pos()
        for i in range(self.steps_taken.size()):
            direction = self.pop_last_direction()                                                       #Get the last direction gone in
            row, col = self.get_pos_of_location_in_direction(self.get_opposite_direction(direction), (row, col)) #Get the position of the Location that direction came from (using opposite direction)
            self.map[row][col].set_contents('X')                                                        #Set the contents of that Location to X
            temp_stack.push(direction)                                                                  #Put the direction in the temporary stack
        for i in range(temp_stack.size()):                                                          #For every direction popped,
            self.steps_taken.push(temp_stack.pop())                                                     #Put it back on the steps_taken stack in the correct order


    def is_position_in_diary(self, position=0):
        """Checks to see if the provided position is noted in Explorer's position
        diary. If no position is provided, uses Explorer's current position.
        post: Returns True or False."""
        if position == 0:
            position = self.get_pos()
        return position in self.position_diary.keys()


    def add_position_to_diary(self, pos=0):
        """Adds the provided position to the Explorer's position diary, noting the
        following information: what directions are possible to go in from this
        position (list) and what directions have already been visited by the
        Explorer from this position. If no position is provided, assumes current
        location of Explorer.
        pre: pos is a tuple with two int values representing (row, col)."""
        if pos == 0:
            pos = self.get_pos()                                                #If no pos provided, sets to current pos
        if not self.is_position_in_diary():
            self.position_diary[pos] = [self.check_possible_directions(),[]]    #Stores possible directions and an empty list for directions it will travel from the position


    def update_position_diary(self):
        """Updates the position diary to include the direction last gone in,
        both for the previous position (ex, to say that it went 'N'), and the
        current one (ex, came from 'S').
        pre: The Explorer is NOT at its starting position.
        post: Adds a string (ex: 'N') to the second item in the positions' position diary.
        If Explorer at starting position, no changes will be made. If the
        direction is already in the position diary, no changes will be made."""
        if self.steps_taken.size() > 0:               #As long as Explorer is not at its starting point,
            row = self.get_row()                        #References to current position
            col = self.get_col()
            direction = self.steps_taken.top()          #The last direction taken

            if (direction == 'N') and ('N' not in self.position_diary[(row+1, col)][1]):    #If the last step was to the North and North is not yet noted,
                self.position_diary[(row+1,col)][1].append('N')                                 #Add it as a direction taken by Explorer from the previous location
                if 'S' not in self.position_diary[(row, col)][1]:                               #If South is not yet noted as a direction visited from new location,
                    self.position_diary[(row,col)][1].append('S')                                   #Add it

            elif (direction == 'E') and ('E' not in self.position_diary[(row, col-1)][1]):  #Same as above, but with East from previous position
                self.position_diary[(row,col-1)][1].append('E')
                if 'W' not in self.position_diary[(row, col)][1]:
                    self.position_diary[(row,col)][1].append('W')

            elif (direction == 'W') and ('W' not in self.position_diary[(row, col+1)][1]):  #West from previous position
                self.position_diary[(row,col+1)][1].append('W')
                if 'E' not in self.position_diary[(row, col)][1]:
                    self.position_diary[(row,col)][1].append('E')

            elif (direction == 'S') and ('S' not in self.position_diary[(row-1, col)][1]):  #South from previous position
                self.position_diary[(row-1,col)][1].append('S')
                if 'N' not in self.position_diary[(row, col)][1]:
                    self.position_diary[(row,col)][1].append('N')


    def are_directions_unexplored(self):
        """Checks its diary to see if Explorer has already been in all possible
        directions from the current location.
        post: Returns True or False."""
        pos = self.get_pos()
        return len(self.position_diary[pos][0]) != len(self.position_diary[pos][1])


    def check_possible_directions(self):
        """Checks the possible directions from the Explorer's current location.
        Returns these directions as strings ('N', for example) in a list.
        post: returns a list that is empty (if there are walls all around the
        current spot) or a list containing strings."""
        current_row = self.get_row()
        current_col = self.get_col()
        directions = []
        if self.map[current_row-1][current_col].get_contents() != 'W':  #If no wall in this direction, count it as an option
            directions.append('N')
        if self.map[current_row][current_col+1].get_contents() != 'W':
            directions.append('E')
        if self.map[current_row][current_col-1].get_contents() != 'W':
            directions.append('W')
        if self.map[current_row+1][current_col].get_contents() != 'W':
            directions.append('S')
        return directions


    def decide_where_to_go(self):
        """Explorer decides where to move from current Location. Returns one of
        the following strings:
            1. 'N', 'E', 'W', 'S' (choosing the first one it has not yet been to)
            2. 'Backtrack' (has tried all possible directions already)
            3. 'None' (tried all posible directions and is at starting point)
        pre: The current position is in the position diary.
        post: Returns a string from above list."""
        pos_diary = self.position_diary
        pos = self.get_pos()
        if not(self.are_directions_unexplored()) and self.steps_taken.size() == 0: #If there are no more directions to explore AND Explorer is at starting point
            return 'No'                                                             #Return empty string
        elif not(self.are_directions_unexplored()):                             #If there are no more directions to explore,
            return 'Backtrack'                                                      #Return 'Backtrack'
        else:                                                                   #Otherwise,
            for direction in self.DIRECTIONS:                                       #For every direction in 'NEWS'
                if (direction in pos_diary[pos][0]) and (direction not in pos_diary[pos][1]):   #If it's not yet been traveled to,
                    return direction                                                                #Return the direction


    def get_opposite_direction(self, direction):
        """Returns the opposite direction of the provided direction.
        pre: direction is one of the following: 'N', 'S', 'E', 'W'
        post: returns a string of one character."""
        return self.DIRECTION_OPP[direction]


    def pop_last_direction(self):
        """Returns the last direction Explorer moved in, as long as it is not at
        its starting point.
        post: returns a string of one character: N, W, E, or S."""
        return self.steps_taken.pop()


    def display_map(self):
        """Prints the current state of the map.
        pre: map is a valid map that can be used by an Explorer (a tuple of tuples
        (of same lengths) containing Locations.)
        post: Outputs the map to the screen."""
        map = self.map
        for row in map:
            for loc in row:
                print(loc.get_contents(), end="")
                if loc.get_contents() == 'X':       #Now that it's printed, if a path to a treasure was displayed,
                    loc.set_contents('.')               #Change it back to a normal path for future adventuring
            print('\n', end="")
        print('\n', end="")
