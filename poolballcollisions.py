def solution(dimensions, your_position, trainer_position, distance):
    import fractions
    
    # Imagine you are shooting the pool bar at position o* and you are trying to hit the pool ball at position x*. 
    # If the pool ball can go up to distance d, how many initial trajectories are possible that hit x without crossing the spot where o started?
    
    #   |----|----|----|----|
    # 2 |    |    | x* |    |
    #   |----|----|----|----|
    # 1 |    | o* |    |    |
    #   |----|----|----|----|
    # 0 |    |    |    |    |
    #   |----|----|----|----|
    #     0    1    2    3
    
    # We can extend the grid in all directions using reflection to avoid calculating the angle at which a ball bounces off the wall:
    
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 2 |    |    | x  |    | x  |    |    |    | x  |    | x  |    |    |    | x  |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 1 |    | o  |    |    |    | o  |    | o  |    |    |    | o  |    | o  |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 0 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 1 |    | o  |    |    |    | o  |    | o  |    |    |    | o  |    | o  |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 2 |    |    | x  |    | x  |    |    |    | x* |    | x  |    |    |    | x  |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 1 |    | o  |    |    |    | o  |    | o* |    |    |    | o  |    | o  |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 0 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 1 |    | o  |    |    |    | o  |    | o  |    |    |    | o  |    | o  |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 2 |    |    | x  |    | x  |    |    |    | x  |    | x  |    |    |    | x  |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 1 |    | o  |    |    |    | o  |    | o  |    |    |    | o  |    | o  |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    # 0 |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
    #   |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
    #     0    1    2    3    2    1    0    1    2    3    2    1    0    1    2    3
    
    # Now the problem can be restated as "starting from o*, how many x or x* can you hit without first hitting an o or a different x where the length of the line is <= d?"
    # My solution is as follows:
    # 1. Move the origin to your original position o.
    # 2. Expand the board recursively, adding new reflected positions until the previous board(s) is surrounded on all sides by a new layer of boards. 
    # 3. After each expansion, calculate all integer bearings (x,y) leading to the reflected positions by computing the reduced form of y/x.
    # 4. Count each bearing to a reflected "x" that isn't also a bearing to a reflected "o" or a reflected bearing from any previous layer.
    
    # Notes: I tried a separate solution which takes advantage of the fact that the straight path to coprime coordinates does not pass any integer lattice point.
    # It may have been faster, but the added complexity wasn't worth it. The "magic" of the solution I've provided here is that since we expand the grid outwardly,
    # we don't need to worry about a ball hitting an x on the way to an o. If the ball has hit an x in a previous layer, step 4 will preclude the path.
    # Furthermore, no path exists where a ball hits an x on the way to an o in the same layer. This is a subtle but important point.
    
    # This is not a particularly efficient solution in time or in space since we store coordinates in a set of tuples. It is more efficient to store the x
    # and y coordinates in two separate sets (two 1000 length sets vs. one 1,000,000 length set) taking advantage of the fact that xs and os have lots of common coordinates.
    # However, this makes it difficult to expand the board outwardly so it requires more code to check whether the first collision on a path was an x or an o. 
    # The collision checking can be simplified by observing that the path only crosses gcd(x,y) integer lattice points. If I didn't have a day job I would 
    # see if that solution works and if so whether it is more performant.
    
    # Finally, with the smallest possible board [2,3] and the largest possible distance (10,000), we exceed maximum recursion depth on Colab.

    def expandboard(layer): # expand board outwardly in layers
        boardpositions = set()
        for i in range(-1 * layer, layer + 1):
            boardpositions.update([((i, -1 * layer)), ((i, layer)), ((-1 * layer, i)), ((layer, i))]) # add bottom, top, left and right rows, set gets rid of duplicates
        your_new_positions = []
        trainer_new_positions = []
        for board in boardpositions:
            flipx, flipy = board[0] % 2, board[1] % 2 # 0 is normal orientation, 1 is reflected
            your_new_position = (board[0] * dimensions[0] + flipx * (dimensions[0] - 2 * your_position[0]),
                                 board[1] * dimensions[1] + flipy * (dimensions[1] - 2 * your_position[1]))
            trainer_new_position = (board[0] * dimensions[0] + (1 - flipx) * trainer_position[0] + flipx * (dimensions[0] - trainer_position[0]) - your_position[0],
                                    board[1] * dimensions[1] + (1 - flipy) * trainer_position[1] + flipy * (dimensions[1] - trainer_position[1]) - your_position[1])
            if your_new_position[0] ** 2 + your_new_position[1] ** 2 <= distancesquared:
                your_new_positions.append(your_new_position)
            if trainer_new_position[0] ** 2 + trainer_new_position[1] ** 2 <= distancesquared:
                trainer_new_positions.append(trainer_new_position)
        return your_new_positions, trainer_new_positions
    
    def calculate_gcd(direction): # Python 2.7 does not have math.gcd (which always returns a positive result).
        gcd = abs(fractions.gcd(direction[0], direction[1]))
        return gcd
    
    def calculate_directions(position, gcd):
        return ((position[0] // gcd, position[1] // gcd))
    
    def countnewdirections(your_positions, trainer_positions):
        your_gcds = list(map(calculate_gcd, your_positions))
        your_directions = list(map(calculate_directions, your_positions, your_gcds))
        ignoredirections.update(your_directions)
        trainer_gcds = list(map(calculate_gcd, trainer_positions))
        trainer_directions = set(map(calculate_directions, trainer_positions, trainer_gcds))
        trainer_directions.difference_update(ignoredirections)
        number = len(trainer_directions) # number of accepted collisions
        ignoredirections.update(trainer_directions)
        return number
    
    def solver(layer, your_positions, trainer_positions, count):
        count += countnewdirections(your_positions, trainer_positions)
        layer += 1
        your_positions, trainer_positions = expandboard(layer)
        if len(your_positions) == 0 and len(trainer_positions) == 0: # stop recursion when no more positions are within a circle of radius distance
            return count
        count = solver(layer, your_positions, trainer_positions, count)
        return count
    
    count = 0
    layer = 0
    distancesquared = distance**2 # precompute this to save a small amount of time
    ignoredirections = set()
    your_positions = set()
    trainer_positions = {tuple(trainer_position[i] - your_position[i] for i in range(2))} # move origin
    
    if list(trainer_positions)[0][0]**2 + list(trainer_positions)[0][1]**2 > distancesquared: # handle edge case where we can't reach the trainer at all
        return 0
    
    return solver(0, your_positions, trainer_positions, count)
