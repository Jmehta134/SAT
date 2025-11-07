from tarjan import tarjan
import copy

def sat(clauses, length=0):
    
    def two_sat(nb_vars):
        # Determine the number of variables
        for i in literals:
            bin_add([i,i])

        # Initialize the graph with nodes for all possible literals
        graph = {lit: [] for i in range(1, nb_vars + 1) for lit in (i, -i)}

        # Build the implication graph from the two_clauses
        for i, j in two_clauses:
            graph[-i].append(j)
            graph[-j].append(i)
        # Find the Strongly Connected Components (SCCs)
        # This returns a list of lists, e.g., [[3, -4], [2], [-1, 1], ...]
        sccs = tarjan(graph)
        # *** FIX: Create a map from each literal to its component's ID ***
        # The SCCs are returned in reverse topological order.
        component_map = {}
        for component_id, scc in enumerate(sccs):
            for node in scc:
                component_map[node] = component_id
        # Check for contradictions
        for i in range(1, nb_vars + 1):
            if component_map[i] == component_map[-i]:
                return None  # Unsatistwo_clauses, literals = [], []fiable

        # Build a valid assignment if no contradictions were found
        solution = []
        for i in range(1, nb_vars + 1):
            # A variable is True if its negation's component appears before its own
            # in the reverse topological sort (i.e., has a higher component ID).
            solution.append(component_map[-i] > component_map[i])
            
        return solution

    def dfs(graph, node):
        if node not in graph :
            return False
        
        stack = [node]
        visited = set()
        while stack :
            current_node = stack.pop()

            if current_node == -node:
                return True
            
            if current_node not in visited : 
                visited.add(current_node)

                for neighbor in graph.get(current_node, []):
                    if neighbor not in visited :
                        stack.append(neighbor)
        return False

    def un2sat(clauses):
        all_literals, unass = [], []
        # Determine the number of variables
        if clauses:
            for clause in clauses:
                for literal in clause:
                    if abs(literal) not in all_literals:
                        all_literals.append(abs(literal))

        # Initialize the graph with nodes for all possible literals
        graph = {i: [] for literal in all_literals for i in (literal, -literal)}
        # Build the implication graph from the clauses
        for i, j in clauses:
            graph[-i].append(j)
            graph[-j].append(i)
        # Find the Strongly Connected Components (SCCs)
        # This returns a list of lists, e.g., [[3, -4], [2], [-1, 1], ...]
        sccs = tarjan(graph)
        # *** FIX: Create a map from each literal to its component's ID ***
        # The SCCs are returned in reverse topological order.
        index = {}
        for component_id, scc in enumerate(sccs):
            for node in scc:
                index[node] = component_id


        # Check for contradictions
        for i in all_literals:
            if index[i] == index[-i]:
                return 0  # Unsatisfiable

        # Get a un sat assignment if no contradictions were found
        # Return value set true unsatisfies the instance.
        for i in all_literals:
            if dfs(graph, i) :
                unass.append(-i)
            elif dfs(graph, -i) :
                unass.append(i)
            
        return sorted(unass)

    def bin_in(val):
        if isinstance(val, (int)):
            low, mid, high = 0, 0, len(literals) - 1
            while low <= high:
                mid = (low + high) // 2 
                if literals[mid] == val:
                    return True
                elif literals[mid] < val:
                    low = mid + 1
                else:
                    high = mid - 1
            return False
        
        low, mid, high = 0, 0, len(two_clauses) - 1
        while low <= high:
            mid = (low + high) // 2
            if two_clauses[mid] == val:
                return True
            elif two_clauses[mid][0] < val[0] or (two_clauses[mid][0]==val[0] and two_clauses[mid][1] < val[1]):
                low = mid + 1
            else:
                high = mid - 1
        return False

    def bin_add(val):
        if isinstance(val, (int)):
            low, mid, high = 0, 0, len(literals) - 1
            while low <= high:
                mid = (low + high) // 2 
                if literals[mid] == val:
                    return 
                elif literals[mid] < val:
                    low = mid + 1
                else:
                    high = mid - 1
            literals.insert(mid, val)
            return

        low, mid, high = 0, 0, len(two_clauses) - 1
        while low <= high:
            mid = (low + high) // 2
            if two_clauses[mid] == val:
                return
            elif two_clauses[mid][0] < val[0] or (two_clauses[mid][0]==val[0] and two_clauses[mid][1] < val[1]):
                low = mid + 1
            else:
                high = mid - 1
        two_clauses.insert(mid, val)

    

    def fact_3sat(clauses, n):
        two_sat = []
        for clause in clauses:
            if n in clause:
                clause.remove(n)
                two_sat.append(clause)
        return sorted(two_sat)

    def sat_3sat(clauses):
        nb_vars = max(abs(x) for clause in clauses for x in clause)
        three_sat = []
        for clause in clauses: 
            if len(clause) == 3 :
                three_sat.append(clause)
                continue
            elif len(clause) == 2 :
                three_sat.append(clause + clause[0:1])
                continue
            elif len(clause) == 1 :
                three_sat.append(clause * 3)
                continue
            three_sat.append(clause[0:2]+[-(nb_vars+1)])
            for i in range(2,len(clause)-2):
                three_sat.append([(nb_vars+1)]+[clause[i]]+[-(nb_vars+2)])
                nb_vars += 1
            three_sat.append([(nb_vars+1)]+clause[-2:])
        return three_sat

    def first_d(clauses):
        sat = []
        nb_vars = max(abs(lit) for clause in clauses for lit in clause)
        for i in range(1, nb_vars+1):
            sat = fact_3sat(copy.deepcopy(clauses), i)
            unval = un2sat(sat)
            if  unval == 0:
                bin_add(i)
            else :
                for j in unval:
                    if i==j:
                        bin_add(i)
                    else :
                        bin_add([min(i,j),max(i,j)])

        for i in range(-nb_vars, 0):
            sat = fact_3sat(copy.deepcopy(clauses), i)
            unval = un2sat(sat)
            if  unval == 0:
                bin_add(i)
            else :
                for j in unval:
                    if i==j:
                        bin_add(i)
                    else :
                        bin_add([min(i,j),max(i,j)])
        

    def depend_search(clauses) :
        for clause in clauses:
                if bin_in(-clause[0]):
                    if bin_in(-clause[1]):
                        if bin_in(-clause[2]):
                            return False, None
                        else :
                            bin_add(clause[2])
                    elif bin_in(-clause[2]):
                        bin_add(clause[1])
                    elif bin_in([min(-clause[1],clause[2]), max(-clause[1],clause[2])]):
                        bin_add(clause[2])
                        two_clauses.remove([min(-clause[1],clause[2]), max(-clause[1],clause[2])])
                    elif bin_in([min(clause[1],-clause[2]), max(clause[1],-clause[2])]):
                        bin_add(clause[1])
                        two_clauses.remove([min(clause[1],-clause[2]), max(clause[1],-clause[2])])
                    else :
                        bin_add([min(clause[1],clause[2]), max(clause[1],clause[2])])
                elif bin_in(-clause[1]):
                    if bin_in(-clause[2]):
                        bin_add(clause[0])
                    elif bin_in([min(-clause[0],clause[2]), max(-clause[0],clause[2])]):
                        bin_add(clause[2])
                        two_clauses.remove([min(-clause[0],clause[2]), max(-clause[0],clause[2])])
                    elif bin_in([min(clause[0],-clause[2]), max(clause[0],-clause[2])]):
                        bin_add(clause[0])
                        two_clauses.remove([min(clause[0],-clause[2]), max(clause[0],-clause[2])])
                    else :
                        bin_add([min(clause[0],clause[2]), max(clause[0],clause[2])])
                elif bin_in(-clause[2]):
                    if bin_in([min(-clause[0],clause[1]), max(-clause[0],clause[1])]):
                        bin_add(clause[1])
                        two_clauses.remove([min(-clause[0],clause[1]), max(-clause[0],clause[1])])
                    elif bin_in([min(clause[0],-clause[1]), max(clause[0],-clause[1])]):
                        bin_add(clause[0])
                        two_clauses.remove([min(clause[0],-clause[1]), max(clause[0],-clause[1])])
                    else :
                        bin_add([min(clause[0],clause[1]), max(clause[0],clause[1])])

    def first_d_set(clauses):
        sat = []
        nb_vars = max(abs(lit) for clause in clauses for lit in clause)
        for i in range(1, nb_vars+1):
            sat = fact_3sat(copy.deepcopy(clauses), i)
            unval = un2sat(sat)
            if  unval == 0:
                literals.add(i)
            else :
                for j in unval:
                    if i==j:
                        literals.add(i)
                    else :
                        two_clauses.add((min(i,j),max(i,j)))

        for i in range(-nb_vars, 0):
            sat = fact_3sat(copy.deepcopy(clauses), i)
            unval = un2sat(sat)
            if  unval == 0:
                literals.add(i)
            else :
                for j in unval:
                    if i==j:
                        literals.add(i)
                    else :
                        two_clauses.add((min(i,j),max(i,j)))
        

    def depend_search_set(clauses) :
        for clause in clauses:
                if (-clause[0]) in literals:
                    if (-clause[1]) in literals:
                        if (-clause[2]) in literals:
                            return False, None
                        else :
                            literals.add(clause[2])
                    elif (-clause[2]) in literals:
                        literals.add(clause[1])
                    elif ((min(-clause[1],clause[2]), max(-clause[1],clause[2]))) in two_clauses:
                        literals.add(clause[2])
                        two_clauses.remove((min(-clause[1],clause[2]), max(-clause[1],clause[2])))
                    elif ((min(clause[1],-clause[2]), max(clause[1],-clause[2]))) in two_clauses:
                        literals.add(clause[1])
                        two_clauses.remove((min(clause[1],-clause[2]), max(clause[1],-clause[2])))
                    else :
                        two_clauses.add((min(clause[1],clause[2]), max(clause[1],clause[2])))
                elif (-clause[1]) in literals:
                    if (-clause[2]) in literals:
                        literals.add(clause[0])
                    elif ((min(-clause[0],clause[2]), max(-clause[0],clause[2]))) in two_clauses:
                        literals.add(clause[2])
                        two_clauses.remove((min(-clause[0],clause[2]), max(-clause[0],clause[2])))
                    elif ((min(clause[0],-clause[2]), max(clause[0],-clause[2]))) in two_clauses:
                        literals.add(clause[0])
                        two_clauses.remove((min(clause[0],-clause[2]), max(clause[0],-clause[2])))
                    else :
                        two_clauses.add((min(clause[0],clause[2]), max(clause[0],clause[2])))
                elif (-clause[2]) in literals:
                    if ((min(-clause[0],clause[1]), max(-clause[0],clause[1]))) in two_clauses:
                        literals.add(clause[1])
                        two_clauses.remove((min(-clause[0],clause[1]), max(-clause[0],clause[1])))
                    elif ((min(clause[0],-clause[1]), max(clause[0],-clause[1]))) in two_clauses:
                        literals.add(clause[0])
                        two_clauses.remove((min(clause[0],-clause[1]), max(clause[0],-clause[1])))
                    else :
                        two_clauses.add((min(clause[0],clause[1]), max(clause[0],clause[1])))

    nb_vars = max(abs(lit) for clause in clauses for lit in clause)
    three_sat = sat_3sat(clauses)
    nb_vars_3sat = max(abs(lit) for clause in three_sat for lit in clause)
    two_clauses, literals = [], []
    if length == 1:
        two_clauses, literals = set(), set()
        first_d_set(three_sat)
        if len(literals) == 0 and len(two_clauses) == 0 :
            return True
        depend_search_set(three_sat)
    elif length == 0:
        first_d(three_sat)
        if len(literals) == 0 and len(two_clauses) == 0 :
            return True
        depend_search(three_sat)
    else :
        raise ValueError("second argument in sat() can only be 0 or 1")
    return two_sat(nb_vars_3sat)[:nb_vars]

if '__main__'==__name__ :
    x = [[1,2], [-1,-2], [1,3], [4,5,-3,-2,1], [4,3,5,-1]]
    print(sat(x))
