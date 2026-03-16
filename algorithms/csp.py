from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algorithms.problems_csp import DroneAssignmentCSP


def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
   
    # TODO: Implement your code here
    return None


def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    
    domains = {v: list(d) for v, d in csp.domains.items()}

    def backtrack(assignment):
        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in list(domains[var]):
            if csp.is_consistent(var, value, assignment):
                csp.assign(var, value, assignment)
                prunings = []
                fc_failure = False
                for neighbor in csp.get_neighbors(var):
                    if neighbor not in assignment:
                        for neighbor_val in list(domains[neighbor]):
                            if not csp.is_consistent(neighbor, neighbor_val, assignment):
                                domains[neighbor].remove(neighbor_val)
                                prunings.append((neighbor, neighbor_val))
                        if not domains[neighbor]:
                            fc_failure = True
                            break
                result = None
                if not fc_failure:
                    result = backtrack(assignment)
                csp.unassign(var, assignment)
                for neighbor, val in prunings:
                    domains[neighbor].append(val)
                if result is not None:
                    return result
        return None

    return backtrack({})
def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:
   
 
    def revise(domains, xi, xj):
        revised = False
        for x in list(domains[xi]):
            has_support = any(csp.is_consistent(xj, y, {xi: x}) for y in domains[xj])
            if not has_support:
                domains[xi].remove(x)
                revised = True
        return revised

    def ac3(domains, queue):
        while queue:
            xi, xj = queue.pop(0)
            if revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in csp.get_neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def backtrack(assignment, domains):
        if csp.is_complete(assignment):
            return assignment

        var = csp.get_unassigned_variables(assignment)[0]

        for value in list(domains[var]):
            if csp.is_consistent(var, value, assignment):
                new_assignment = assignment.copy()
                csp.assign(var, value, new_assignment)

                new_domains = {v: list(d) for v, d in domains.items()}
                new_domains[var] = [value]

                queue = [(neighbor, var) for neighbor in csp.get_neighbors(var) if neighbor not in new_assignment]
                if ac3(new_domains, queue):
                    result = backtrack(new_assignment, new_domains)
                    if result is not None:
                        return result
        return None

    initial_domains = {v: list(d) for v, d in csp.domains.items()}
    initial_queue = [(v, n) for v in csp.variables for n in csp.get_neighbors(v)]
    if not ac3(initial_domains, initial_queue):
        return None
    return backtrack({}, initial_domains)


def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    
    # TODO: Implement your code here (BONUS)
    return None
