class NogginCallable:
    # call the function with given arguments
    def call(self, interpreter, arguments):
        raise NotImplementedError
        
    # return the number of parameters the function takes
    def arity(self):
        raise NotImplementedError
    
    # return a string representation of the function
    def __str__(self):
        raise NotImplementedError

class NogginFunction(NogginCallable):
    def __init__(self):
        raise NotImplementedError
    
    # call the function with given arguments
    def call(self, interpreter, arguments):
        raise NotImplementedError
        
    # return the number of parameters the function takes
    def arity(self):
        raise NotImplementedError
    
    # return a string representation of the function
    def __str__(self):
        raise NotImplementedError

class NogginClass(NogginCallable):
    def __init__(self):
        raise NotImplementedError
    
    # call the function with given arguments
    def call(self, interpreter, arguments):
        raise NotImplementedError
        
    # return the number of parameters the function takes
    def arity(self):
        raise NotImplementedError
    
    # return a string representation of the function
    def __str__(self):
        raise NotImplementedError