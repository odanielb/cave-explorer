#-------------------------------------------------------------------------------
# Name:        Location.py
# Purpose: Create a Location class to work with the Explorer module
#
# Author:      odanielb (Bridget O'Daniel)
#-------------------------------------------------------------------------------


class Location(object):


    def __init__(self, row, col, contents):
        """Creates a new Location (a single spot on a map) with a provided row
        and column (position) and the provided contents, which contains one of
        the following appropriate options:
            'W' = Wall
            '.' = Empty path
            'T' = Treasure
            'M' = Explorer
        pre: row and col are ints and the combination is unique to this Location,
        contents contains a string from the above list."""
        self.row = row
        self.col = col
        self.contents = contents


    def get_pos(self):
        """Returns the position of this Location as a tuple, (row, col).
        pre: None
        post: returns the position as a tuple containing two ints."""
        return (self.row, self.col)


    def get_row(self):
        """Returns the row this Location is in.
        post: returns an int."""
        return self.row


    def get_col(self):
        """Returns the column this Location is in.
        post: returns an int."""
        return self.col


    def set_contents(self, contents):
        """Sets the Location to contain to the provided contents.
        pre: Contents must contains a string from the following list:
            'W' = Wall
            '.' = Empty path
            'T' = Treasure
            'M' = Explorer
            'X' = To display path taken to treasure
        post: Sets the Location to be the indicated content."""
        self.contents = contents


    def get_contents(self):
        """Returns the contents of this Location.
        post: A string of one character ('W', '.', 'T', 'M', 'X') is returned."""
        return self.contents


    def __str__(self):
        """Returns a string representing the current Location.
        post: returns a string."""
        dict = {'W':'Wall', '.':'Path', 'T':'Treasure', 'M':'Explorer', 'X':'Display Path'}
        pos = self.get_pos()
        return ""+dict[self.contents]+" at "+str(pos)
