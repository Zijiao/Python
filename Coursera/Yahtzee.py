"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """    
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = [0] * 20
    for die in hand:
        scores[die - 1 ] += die
                
    return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    possible_dice = gen_all_sequences([(num + 1) for num in range(num_die_sides)], num_free_dice)
    possible_scores = [score(held_dice + new_dice) for new_dice in possible_dice]
    denominator = 1.0 / (num_die_sides ** num_free_dice)    
    return sum(possible_scores) * denominator


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([()])
    sorted_sequences = gen_sorted_sequences(range(len(hand)),len(hand))
    positions = get_positions(sorted_sequences)
    for position in positions:
        temp_hold = []
        for elem in position:
            temp_hold.append(hand[elem])
            if tuple(temp_hold) not in holds:
                holds.add(tuple(temp_hold))
    return holds
    

def get_positions(sorted_sequences):
    """
    A function used in gen_all_holds()
    This function takes a sorted sequences return by gen_sorted_sequences 
    and returns all possible positions related to the given hand
    """
    positions = []
    for elem in sorted_sequences:
        temp_position = []
        for num in elem:
            if num not in temp_position:
                temp_position.append(num)
        if temp_position not in positions:
            positions.append(temp_position)
    return positions


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    length = len(hand)
    expected_values = []
    dice_to_hold = []
    all_holds = gen_all_holds(hand)
    for hold in all_holds:
        dice_to_hold.append(hold)
        expected_values.append(expected_value(hold, num_die_sides, length - len(hold)))
        
    max_index = expected_values.index(max(expected_values))
    
    
    return (max(expected_values), tuple(dice_to_hold[max_index]))


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


