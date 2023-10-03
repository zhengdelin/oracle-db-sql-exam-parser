def findIndex(arr: list, cond):
    for i in range(0, len(arr)):
        # print("arr[i]", arr[i], cond(arr[i]))
        if (cond(arr[i])):
            return i
    return None


def find(arr: list, cond):
    index = findIndex(arr, cond)
    return arr[index] if index != None else None


def map(arr: list, fn=lambda i: i):
    newArr = []
    for item in arr:
        newArr.append(fn(item))
    return newArr