"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
            
        self._grid_height = grid_height
        self._grid_width = grid_width
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        for dummy_i in range(self._grid_height):
            for dummy_j in range(self._grid_width):
                self.set_empty(dummy_i, dummy_j)

        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        dummy_i = 0
        while dummy_i < self.num_zombies():
            yield self._zombie_list[dummy_i]
            dummy_i += 1


    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        dummy_i = 0
        while dummy_i < self.num_humans():
            yield self._human_list[dummy_i]
            dummy_i += 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        for dummy_i in range(self._grid_height):
            for dummy_j in range(self._grid_width):
                visited.set_empty(dummy_i, dummy_j)
                
        distance_field = [[self._grid_height * self._grid_width for dummy_i in range(self._grid_width)] for dummy_j in range(self._grid_height)]
        boundary = poc_queue.Queue()
        
        if entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        elif entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
                
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            all_neighbours = self.four_neighbors(current_cell[0], current_cell[1])
            
            for neighbour in all_neighbours:
                if visited.is_empty(neighbour[0], neighbour[1]) and self.is_empty(neighbour[0], neighbour[1]):
                    visited.set_full(neighbour[0], neighbour[1])
                    boundary.enqueue(neighbour)
                    distance_field[neighbour[0]][neighbour[1]] = min(distance_field[neighbour[0]][neighbour[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
        
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index, human in enumerate(self._human_list):
            fake_potential_moves_list = self.eight_neighbors(human[0], human[1])
            fake_potential_moves_list.append((human[0], human[1]))
            potential_moves_list = []
            for potential_move in fake_potential_moves_list:
                if self.is_empty(potential_move[0], potential_move[1]):
                    potential_moves_list.append(potential_move)
            
            max_distance = 0
            potential_moves_dict = {}
            correct_moves_list = []
            for potential_move in potential_moves_list:
                potential_moves_dict[potential_move] = zombie_distance[potential_move[0]][potential_move[1]]
                if zombie_distance[potential_move[0]][potential_move[1]] > max_distance:
                    max_distance = zombie_distance[potential_move[0]][potential_move[1]]
            for potential_move in potential_moves_dict:
                if potential_moves_dict[potential_move] == max_distance:
                    correct_moves_list.append(potential_move)
            final_move = correct_moves_list[random.randrange(len(correct_moves_list))]
            self._human_list[index] = final_move
                    
                    
            
            
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index, zombie in enumerate(self._zombie_list):
            fake_potential_moves_list = self.four_neighbors(zombie[0], zombie[1])
            fake_potential_moves_list.append((zombie[0], zombie[1]))
            potential_moves_list = []
            for potential_move in fake_potential_moves_list:
                if self.is_empty(potential_move[0], potential_move[1]):
                    potential_moves_list.append(potential_move)
            
            min_distance = self._grid_width * self._grid_height
            potential_moves_dict = {}
            correct_moves_list = []
            for potential_move in potential_moves_list:
                potential_moves_dict[potential_move] = human_distance[potential_move[0]][potential_move[1]]
                if human_distance[potential_move[0]][potential_move[1]] < min_distance:
                    min_distance = human_distance[potential_move[0]][potential_move[1]]
            for potential_move in potential_moves_dict:
                if potential_moves_dict[potential_move] == min_distance:
                    correct_moves_list.append(potential_move)
            final_move = correct_moves_list[random.randrange(len(correct_moves_list))]
            self._zombie_list[index] = final_move

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40, None, [(14,15)],[(2,12)]))

