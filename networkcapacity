# toy problem about network capacity.
# Given a list of entrances and exits (ints >= 0) and a matrix of capacities where x_ij is the capacity of the "hallway" between room i and room j, compute
# the maximum capacity of the network per timestep.

def solution(entrances, exits, path):
    # 1. Compute all possible paths that can acommodate >0 bunnies from any entrance to any exit. 
    # 2. Next, determine the capacity of path #1 (number of bunnies per timestep).
    # 3. Next, subtract that capacity from the network.
    # 4. Repeat steps 2-3 for all remaining paths, keeping track of the capacity of each path.
    # 5. Return the total capacity.
    # NOTE: I believe this problem can also be solved by writing a system of linear equations taking 
    # advantage of "conservation of bunnies" -- i.e. the number of bunnies into a room must equal the number
    # of bunnies out of a room. If I was allowed to use numpy I think this method could be faster since there
    # are many optimizations for linear equation solvers.
    startingrooms = entrances
    finalrooms = exits
    network = path
    
    def findpaths(startingroom, finalrooms, network, path=[]): # find all paths from each entrance to any exit using Dijkstra's algorithm
        # path = []
        path = path + [startingroom]
        # print(f'appended room {startingroom} to path {path}')
    
        if startingroom in finalrooms:
            # print(f'appending successful path {path}')
            return [path] # this is bracketed because the second time through, there may be multiple paths in the loop and we don't want them combined
    
        paths = []
    
        for door, capacity in enumerate(network[startingroom]):
            if door in path:
                # print(f'room {door} already visited')
                pass
            elif capacity == 0:
                # print(f'dead end path {path + [door]}')
                pass
            else:
                # print(f'trying room {door}')
                newpaths = findpaths(door, finalrooms, network, path)
                for newpath in newpaths:
                    paths.append(newpath)
                    # print(f'appending successful path {newpaths}')
    
        return paths
    
    def findallpaths(startingrooms, finalrooms, network): 
        paths = []
        for startingroom in startingrooms:
            paths += findpaths(startingroom, finalrooms, network)
        return paths
    
    def findcapacity(route, network): 
        capacity = min([network[route[idx]][route[idx+1]] for idx in range(len(route[:-1]))]) # smallest "hallway" on the bunny route
        for idx in range(len(route[:-1])):
            network[route[idx]][route[idx+1]] -= capacity # subtract capacity of each path from the network
        return capacity, network
    
    paths = findallpaths(startingrooms, finalrooms, network)
    # print(f'Succesful paths: {paths}')
    
    capacity = 0
    for route in paths:
        routecapacity, network = findcapacity(route, network)
        capacity += routecapacity
        # print(f'total capacity is {capacity}')

    return capacity
