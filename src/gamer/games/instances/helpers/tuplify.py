# tests if an object's type is "primitive"
# --> easily encodable into dict
PRIMITIVES = (int, float, str, bool,)
def is_primitive(thing):
    res = type(thing) in PRIMITIVES
    return res

# turn nested list into nested tuple
# doesn't modify inputted board state
def tuplify(input):

    # if list, then recursively convert elts to tuple
    if isinstance(input, list):
        # construct output list, then list --> tuple convert it
        output = []

        # recursive calls
        for elt in input:
            tuplified_elt = tuplify(elt)
            output.append(tuplified_elt)

        # turns main list into tuple
        output = tuple(output)

    # if dict, encode as tuple
    elif isinstance(input, dict):

        # construct output list, then list --> tuple convert it
        output = []

        for key in input.keys().sort():
            tuplified_key = (key, tuplify(input[key]))
            output.append(tuplified_key)

        output = tuple(output)

    # otherwise, return
    elif is_primitive(input):
        output = input

    # assumed input is a custom object
    # --> we demand that a tuplify() method be defined
    else:
        output = input.tuplify()

    # print(output)
    return output
