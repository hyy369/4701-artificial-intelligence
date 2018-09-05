"""
COMS W4701 Artificial Intelligence - Homework 0

In this assignment you will implement a few simple functions reviewing
basic Python operations and data structures.

@author: YOUR NAME (YOUR UNI)
"""


def manip_list(list1, list2):
    # YOUR CODE HERE
    print (list1[-1])     #1
    list1.pop()           #2
    list2[1] = list1[0]   #3
    print(list1 + list2)  #4
    return [list1, list2] #5


def manip_tuple(obj1, obj2):
    # YOUR CODE HERE
    my_tuple = (obj1, obj2)     #1
    my_tuple[0] = "hello world" #2
    return None


def manip_set(list1, list2, obj):
    # YOUR CODE HERE
    set1 = set(list1)     #1
    set2 = set(list2)     #2
    set1.add(obj)         #3
    print (obj in set2)   #4
    print (set1 - set2)   #5
    print (set1 | set2)   #6
    print (set1 & set2)   #7
    set1.discard(obj)     #8
    return None


def manip_dict(tuple1, tuple2, obj):
    # YOUR CODE HERE
    my_dict = dict(zip(tuple1, tuple2)) #1
    print (my_dict[obj])  #2
    my_dict.pop(obj)      #3
    print (len(my_dict))  #4
    my_dict[obj] = 0      #5
    return [(key, my_dict[key]) for key in my_dict] #6

if __name__ == "__main__":
    #Test case
    print(manip_list(["artificial", "intelligence", "rocks"], [4701, "is", "fun"]))

    try: manip_tuple("oh", "no")
    except TypeError: print("Can't modify a tuple!")

    manip_set(["sets", "have", "no", "duplicates"], ["sets", "operations", "are", "useful"], "yeah!")

    print(manip_dict(("list", "tuple", "set"), ("ordered, mutable", "ordered, immutable", "non-ordered, mutable"), "tuple"))
