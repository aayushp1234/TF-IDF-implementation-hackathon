arr=[]
with open('lc.txt',"r") as file:
    for line in file:
        arr.append(line)

def array_with_removed_pattern(array, pattern):
    new_arr=[]
    for element in array:
        if pattern not in array:
            new_arr.append(element)
        else:
            print("Removed element:" + element)
    return new_arr

arr=array_with_removed_pattern(arr,"/solution")

arr=list(set(arr))

with open('lc_problems.txt','a') as m:
    for x in arr:
        m.write(x)
