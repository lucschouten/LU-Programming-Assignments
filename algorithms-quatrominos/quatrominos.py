import numpy as np
import typing

class Quatrominos(object):

    def __init__(self, player0: typing.Set[typing.Tuple[int, int, int, int]],
                 player1: typing.Set[typing.Tuple[int, int, int, int]],
                 board: np.ndarray,
                 player_on_turn: int):
        """
        Initializes the game board, and divides the tiles among both players.
        Each tile is represented as a 1d numpy array, consisting of exactly
        four numbers, where the first number (index 0) is positioned north, the
        second number (index 1) is positioned east, the third number (index 2)
        is positioned south and finally the fourth number (index 3) is
        positioned west. Of course, both players are free to rotate the numbers
        both clockwise and anti-clockwise.

        :param player0: The tiles that are in the hand of player 0
        :param player1: the tiles that are in the hand of player 1
        :param board: The playing board will be a 3-dimensional array, where
        the first two dimensions depict the columns and rows of the game board,
        respectively, and the third dimension is of size 4, representing a
        tile.
        :param player_on_turn: 0 iff player 0 is on turn, 1 otherwise
        """
        self.player_hand = [player0, player1]
        self.board = board
        self.player_on_turn = player_on_turn
        
    def print_current_state(self) -> None:
        """
        Prints the current state, in free format
        """
        formatted_tiles = []
        #store every tile in a formatted way over several lines 
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                tile = [x if x != -1 else " " for x in self.board[row][column]] 
                formatted_tiles.append("+-----+") 
                formatted_tiles.append("|  "            + str(tile[0]) +             "  |")
                formatted_tiles.append("|"+str(tile[3]) +   "   "      +str(tile[1]) + "|")
                formatted_tiles.append("|  "             +str(tile[2]) +             "  |")
                formatted_tiles.append("+-----+")  

        column, row_tile, row_board = 0, 0, 0
        end_of_line = len(self.board) * 5
        end_of_row_tile = 5
        line = []

        while row_board < len(self.board[0]): #print the whole board
            while row_tile < end_of_row_tile: #print all the tiles in a row
                while column < end_of_line: #print one line of all the tiles in a row
                    line.append(formatted_tiles[column])
                    column_copy = column
                    column+=5
                row_tile+=1
                column = row_tile
                line = " ".join(line)
                print(line)
                line = []
            row_board += 1
            column = column_copy + 1
            row_tile = column_copy + 1
            end_of_row_tile = column + 5
            end_of_line = column+len(self.board)*5


    @staticmethod
    def get_rotated_tile(tile: typing.Tuple[int, int, int, int],
                         rotations: int) -> typing.Tuple[int, int, int, int]:
        """
        Returns a tile that is a clock-wise rotation of the input tile. E.g.,
        tile (1, 2, 3, 4) will in case of a single rotation be rotated to
        tile (4, 1, 2, 3)

        :param tile: the input tile to rotate
        :param rotations: the number of rotations (each rotation being a 90
        degree clockwise turn)
        :return: The rotated tile
        """
        while rotations != 0:
            tile = (tile[3], tile[0], tile [1], tile[2])
            rotations = rotations - 1
        return tile

    def adjacent_locations(self) -> typing.Set[typing.Tuple[int, int]]:
        """
        Returns a set with tuples of (y,x)-coordinates where we could
        potentially fit a tile (if the numbers would match). Note that the
        first tile should always be placed in the middle.

        :return: a set with tuples of (y,x)-coordinates of vacant positions
        adjacent to non-vacant positions
        """
        adjacent_vacant_positions = set()
        for row in range(len(self.board)):#row position
            for column in range(len(self.board[row])):#column position
                if (self.board[row][column][0] != -1 and
                    self.board[row][column][1] != -1 and 
                    self.board[row][column][2] != -1 and 
                    self.board[row][column][3] != -1): #position is non-vacant

                    if (row - 1) in range(len(self.board)):#Before looking north, Is the y coord still on the board?
                        if (self.board[row-1][column][0] == -1 and
                            self.board[row-1][column][1] == -1 and
                            self.board[row-1][column][2] == -1 and
                            self.board[row-1][column][3] == -1):#position is vacant
                            adjacent_vacant_positions.add((row-1,column)) #add the north vacant position, row-1 = y coord and column = x coord

                    if (row + 1) in range(len(self.board)):#Before looking south, Is the y coord still on the board?
                         if (self.board[row+1][column][0] == -1 and
                             self.board[row+1][column][1] == -1 and
                             self.board[row+1][column][2] == -1 and
                            self.board[row+1][column][3] == -1):#position is vacant
                            adjacent_vacant_positions.add((row+1,column)) #add the south vacant position, row-1 = y coord and column = x coord

                    if (column - 1) in range(len(self.board[row])):#Before looking west, is the x coord still on the board?
                        if (self.board[row][column-1][0] == -1 and
                            self.board[row][column-1][1] == -1 and
                            self.board[row][column-1][2] == -1 and
                            self.board[row][column-1][3] == -1):#position is vacant
                            adjacent_vacant_positions.add((row,column-1)) #add the west vacant position, row = y coord and column -1 = x coord

                    if (column + 1) in range(len(self.board[row])):#Before looking east, is the x coord still on the board?
                        if (self.board[row][column+1][0] == -1 and
                            self.board[row][column+1][1] == -1 and
                            self.board[row][column+1][2] == -1 and
                            self.board[row][column+1][3] == -1):#position is vacant
                            adjacent_vacant_positions.add((row,column+1)) #add the west vacant position, row = y coord and column +1 = x coord

        if len(adjacent_vacant_positions) == False:#middle position
            if len(self.board) % 2 == 1:
                mid_row_board = int(((len(self.board)-1)/2))
            if len(self.board[0]) % 2 == 1:
                mid_column_board = int(((len(self.board[0])-1)/2))
            adjacent_vacant_positions.add((mid_row_board,mid_column_board))
        return adjacent_vacant_positions

    def boardisempty(self) -> bool:
        """Checks wether the board is empty
        :return: true if the board is empty, false otherwise"""
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                for value in range(len(self.board[row][column])):
                    if self.board[row][column][value] != -1:
                        return False
        return True

    def can_place_given_tile(self, board_y: int, board_x: int,
                             tile: np.array) -> bool:
        """
        Checks whether the tile, in its current orientation, can be placed on
        the indicated position on the board. Note that the numbers of the tile
        are north, east, south, west, respectively.

        :param board_y: board y index to place the tile
        :param board_x: board x index to place the tile
        :param tile: the numpy array representing the tile
        :return: true if the tile can be placed in this orientation on the
        board, false otherwise
        """
        if self.boardisempty(): #if board is empty the tile can be placed
            return True
        elif self.boardisempty() == False and (board_y,board_x) in self.adjacent_locations(): #checks the tile is in adjacent locations (and can be placed adjacent to a tile)
            if (board_y - 1) in range(len(self.board)) and self.board[board_y-1][board_x][2] != -1:
                if self.board[board_y-1][board_x][2] != tile[0]:
                    return False
            if (board_y + 1) in range(len(self.board)) and self.board[board_y+1][board_x][0] != -1:
                if self.board[board_y+1][board_x][0] != tile[2]:
                    return False
            if (board_x - 1) in range(len(self.board[board_y])) and self.board[board_y][board_x-1][1] != -1:
                if self.board[board_y][board_x-1][1] != tile[3]:
                    return False
            if (board_x + 1) in range(len(self.board[board_y])) and self.board[board_y][board_x+1][3] != -1:
                if self.board[board_y][board_x+1][3] != tile[1]:
                    return False
            return True
        elif self.boardisempty and (board_y,board_x) not in self.adjacent_locations():
            return False
        else:
            return True

    def count_available_moves(self, tiles: np.array) -> int:
        """
        Counts the number of moves that can be made, with the tiles provided.
        Note that a tile can be placed in various orientations. Different
        orientations count as different moves.

        :param tiles: A numpy array with the tiles
        :return: The number of moves a player can make
        """
        set_of_options = list()
        number_of_available_moves = 0
        for tile in tiles:
            for rotation in range(4): 
                set_of_options.append(self.get_rotated_tile(tile,rotation))

        for option in set_of_options:
            for position in self.adjacent_locations():
                if self.can_place_given_tile(position[0],position[1],option) == True:
                    number_of_available_moves += 1
        return number_of_available_moves

    def check_current_player_lost(self) -> bool:
        """
        Determines whether the player that is currently on turn has lost the
        game. That can either happen by the other player having played all
        their tiles, or the current player having no available moves.

        :return: True iff the current player has lost, False otherwise
        """
        other_player = 1 - self.player_on_turn
        current_player_hand = self.player_hand[self.player_on_turn] #set of tiles
        other_player_hand = self.player_hand[other_player]

        if ((self.count_available_moves(current_player_hand) == 0 and len(current_player_hand) != 0) or #player can't do a move but still has tiles
           (len(other_player_hand) == 0 and len(current_player_hand) > 0)): #other player has no tiles left while current player has
            return True
        else:
            return False
    
    def current_player_can_win(self) -> bool:
        """
        Uses a exhaustive search algorithm to determine which player will win,
        if both players adopt an optimal strategy. Use a recursive function.
        See the slides of lecture 3 to find pseudo-code for this algorithm.
        Ensure that after this function, all class variables that were changed
        are set back to their original values.

        :return: True iff the player on turn can win
        """
        other_player = 1 - self.player_on_turn 

        if self.check_current_player_lost() == True: #game ended, player on move has lost
            return False

        else: #game not ended, there are still possible moves
            copy_player_hand = self.player_hand[self.player_on_turn].copy()

            for location in self.adjacent_locations(): 
                for tile in copy_player_hand:
                    check_unique_rotation = set() #set where the unique rotations of a tile can be stored
                    rotation_tile = self.get_rotated_tile(tile, 1)
                    check_unique_rotation.add(rotation_tile) #adds the first 90 degree rotation of the tile to a set
                    for rotation in range(4): 
                        tile2 = self.get_rotated_tile(tile, rotation)
                        check_unique_rotation.add(tile2)#adds the rotation of the tile
                        if self.can_place_given_tile(location[0], location[1], tile2) == True: #try possible rotations of all available tiles on all adjacent locations
                            self.player_hand[self.player_on_turn].remove(tile) 
                            copy_board = np.copy(self.board) 
                            player0_hand = self.player_hand[0].copy()
                            player1_hand = self.player_hand[1].copy()
                            self.player_hand[self.player_on_turn].add(tile)
                            copy_game = Quatrominos(player0_hand, player1_hand, copy_board, other_player) #make a copy of the object to playout the game
                            copy_game.board[location[0]][location[1]] = tile2 
                            if not copy_game.current_player_can_win(): #recursively determine if the current player can win
                                return True
                            if len(check_unique_rotation) > 1: #checks wether a tile has unique rotations (so the rotation isn't equal to the normal tile, like 2,2,2,2)
                                continue #if the tile isn't equal to its rotation (len(set) is bigger than 1) skip to the next rotation of the tile
                            else:
                                break #if the tile is equal to its rotation (len(set) is equal to 1) skip to the next tile
            return False 

    def best_move_greedy(self) -> typing.Tuple[int, int, np.array]:
        """
        OPTIONAL. Design a greedy function to determine the best way. This
        algorithm involves enumerating all possible moves, and determining
        which of the moves seems good, without looking further ahead. A logical
        greedy approach would be, e.g., select the move that leaves the other
        player with the least possible amount of free moves.

        :return: A 3-tuple, containing the (y, x) coordinate of the tile, and
        the tile in its proper orientation
        """
        other_player = 1 - self.player_on_turn         
        possible_moves_other_player = float("inf") 
        tile_best_move = None 
        location_best_move = None

        for location in self.adjacent_locations(): 
            for tile in self.player_hand[self.player_on_turn]:
                for rotation in range(4):
                    tile = self.get_rotated_tile(tile, rotation)
                    if self.can_place_given_tile(location[0], location[1], tile) == True: #try all possible rotations of all available tiles on all adjacent locations
                        copy_board = np.copy(self.board) 
                        self.board[location[0]][location[1]] = tile #do move
                        moves_other_player_for_move = self.count_available_moves(self.player_hand[other_player])
                        if moves_other_player_for_move < possible_moves_other_player: #compare available moves of the opponent with the move before
                            #move that leaves the oponnent with less possible moves
                            possible_moves_other_player = moves_other_player_for_move  
                            tile_best_move = tile 
                            location_best_move = location
                        self.board = copy_board #undo move
        return (location_best_move[0], location_best_move[1], tile_best_move) #return "best" move
