# all of the following functions are non-destructive
# and do not mutate the values of existing objects

# given a list:
# return reversed version of list
# while keeping order of nested lists
# return [] for blank list
def myreverse(l1):
    # compose and return new list by iterating old list from back to front
    l2 = [l1[i] for i in range(len(l1) - 1, -1, -1)]
    return l2

# given a list:
# return mirrored version of list with all values reversed
# including those inside nested lists of any depth
# return [] for blank list
def mirror(l1):
    # compose and return new list by iterating old list from back to front
    # and recursively repeat process on any nested list
    if isinstance(l1, list):
        l2 = [mirror(l1[i]) for i in range(len(l1) - 1, -1, -1)]
        return l2
    # return initial object if not a list
    return l1

# given a list:
# return version of list with no nesting
# and all nested values extracted to outermost list
# return [] for blank list
def flatten(l1):
    return

# given a list:
# return version of list with only integer values
# return None if no integers are present
def int_list(l1):
    return

# given a dict:
# return version of dict with keys and values swapped
def invert_dict(d1):
    return

l1 = [1, 2, [3, 4, [5, 6]], [[7, 8], 9]]
print(myreverse(l1))
print(mirror(l1))
