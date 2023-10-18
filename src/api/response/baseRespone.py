from typing import List, TypeVar, Generic

T = TypeVar('T')

class Response(Generic[T]) :
    def __init__(self, status_code : int, data : T) : 
        self.status_code = status_code
        self.data = data