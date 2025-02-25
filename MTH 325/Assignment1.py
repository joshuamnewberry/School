#Start a comment here
def Havel_Hakimi(input_list):
    return True

#Test cases begin here

#Havel_Hakimi([2,2])) should return False
print(Havel_Hakimi([2,2]), "| False")

#Havel_Hakimi([1,1,1,1])) should return True
print(Havel_Hakimi([1,1,1,1]), "| True")

#Havel_Hakimi([1,1,1,1,1,1,1,1,1]) should return False
print(Havel_Hakimi([1,1,1,1,1,1,1,1,1]), "| False")

#Havel_Hakimi([6,5,4,3,3,2,1]) should return True
print(Havel_Hakimi([6,5,4,3,3,2,1]), "| True")

#Havel_Hakimi([0,0,0,0,0,0]) should return True
print(Havel_Hakimi([0,0,0,0,0,0]), "| True")

#Havel_Hakimi([6,5,4,3,2,2]) should return False
print(Havel_Hakimi([6,5,4,3,2,2]), "| False")

#Havel_Hakimi([8,7,6,5,4,4,2,1,1]) should return False
print(Havel_Hakimi([8,7,6,5,4,4,2,1,1]), "| False")

#Havel_Hakimi([5,5,5,5,4,3]) should return False
print(Havel_Hakimi([5,5,5,5,4,3]), "| False")

#Havel_Hakimi([5,5,5,5,4,3]) should return True
print(Havel_Hakimi([5,5,5,5,4,4]), "| True")

#Havel_Hakimi([3,3,3,3,3,3,3,3,3,3]) should return True
print(Havel_Hakimi([3,3,3,3,3,3,3,3,3,3],), "| True")