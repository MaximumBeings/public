#Enter a and b as strings
def multi( a, b):
    y = []
    y2 = []
    y3 = 0
    y4 = 0
    ans = 0
    for x in list(a):
        y.append(int(x))
    for x in list(b):
        y2.append(int(x))
    
    for x in range(len(y)):
        y3 += y[x]
        
    for x in range(len(y2)):
        y4 += y2[x]
        
    ans = y3 * y4
    return ans
 
#Sample calls will be like so
multi( '11', '11')    
multi( '22', '22')
multi( '33', '33') 
    
    