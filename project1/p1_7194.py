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
    # return non-list object unchanged to handle recursive cases
    return l1

# given a list:
# return version of list with no nesting
# and all nested values extracted to outermost list
# return [] for blank list
def flatten(l1):
    # compose and return new list by iterating old list in order
    # and recursively extracting all nested values to parent
    if isinstance(l1, list):
        l2 = [j for i in l1 for j in flatten(i)]
        return l2
    # return non-list object enclosed in list for recursive cases
    return [l1]

# given a list:
# return version of list with only integer values
# return None if no integers are present
def int_list(l1):
    # compose and return new list by getting iterating old list in order
    # and only getting integer values
    l2 = [i for i in l1 if isinstance(i, int)]
    if len(l2):
        return l2
    # return None if no integers are found
    return None

# given a dict:
# return version of dict with keys and values swapped
def invert_dict(d1):
    return {d1[i]: i for i in d1}
