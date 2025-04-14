from typing import List, Any

## Stealing my Queue Class from CIS 163 instead of importing something
class Queue:
    def __init__(self, lst:list = None) -> None:
        if lst == None:
            lst = []
        if type(lst) != list:
            return TypeError
        self.__lst = lst
    
    def __str__(self) -> str:
        return str(self.__lst)
    
    @property
    def queue(self) -> list:
        return self.__lst
    @queue.setter
    def queue(self, lst:list) -> None:
        if type(lst) != list:
            return TypeError
        self.__lst = lst
    
    @property
    def size(self) -> int:
        return len(self.__lst)
    
    @property
    def front(self) -> Any:
        if self.size == 0:
            raise IndexError
        return self.__lst[0]
    
    @property
    def rear(self) -> Any:
        if self.size == 0:
            raise IndexError
        return self.__lst[self.size-1]
    
    def add(self, element:Any) -> None:
        self.__lst.append(element)
    
    def remove(self, num:int = 1) -> Any|List[Any]:
        if num > self.size:
            raise ValueError("Not enough values in the queue")
        lst = []
        for _ in range (0, num):
            lst.append(self.__lst.pop(0))
        if len(lst) == 1:
            return lst[0]
        return lst
    
    def pop(self, num:int = 1) -> Any|List[Any]:
        return self.remove(num)

## End Queue



## Actual Assignment material

# Input from 1 to N in dictionary adjacency list format
def topological_sort(graph:dict) -> List[int]:
    in_degree = dict()
    topological_order = []
    queue = Queue()

    for i in range (1, len(list(graph.keys()))+1):
        in_degree[i] = 0
    
    for key in graph:
        for ele in graph[key]:
            in_degree[ele] += 1
    
    for key in in_degree:
        if in_degree[key] == 0:
            queue.add(key)
    
    while queue.size > 0:
        curr_ele = queue.pop()
        topological_order.append(curr_ele)

        for vertex in graph[curr_ele]:
            in_degree[vertex] -= 1
            if in_degree[vertex] == 0:
                queue.add(vertex)
    
    if len(topological_order) != len(list(graph.keys())):
        raise ValueError("Graph has a cycle or is not fully connected.")
    
    return topological_order

graph = dict()
graph[1] = [2, 3, 4]
graph[2] = [4, 5]
graph[3] = [6]
graph[4] = [3, 6, 7]
graph[5] = [4, 7]
graph[6] = []
graph[7] = [6]
print(f"Topological Sorting: {topological_sort(graph)}")