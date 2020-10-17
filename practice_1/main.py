import math
doc_1 = [2, 5, 0, 0, 0]
doc_2 = [0, 1, 0, 2, 3]
doc_3 = [2, 5, 0, 0, 0]

def v_sum(v1,v2):
    result = 0
    for i in range(len(v1)):
        result += (v1[i]*v2[i])
    return result

def cos_measure(v1, v2):
    wT = math.sqrt(sum([i**2 for i in v1] ))
    rT = math.sqrt(sum([i**2 for i in v2] ))    
    return v_sum(v1,v2)/(wT*rT)

print ("doc_1, doc_3 :",cos_measure(doc_1, doc_3))
print ("doc_1, doc_2 :",cos_measure(doc_1, doc_2))
