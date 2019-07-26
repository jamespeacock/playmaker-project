
def make_iterable(data):
    if type(data) == list:
        return data
    else:
        return [data]