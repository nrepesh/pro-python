# # State Pattern 

# # Bad Example 

# from enum import Enum 

# class DocumentState(Enum): 
#     DRAFT = 1
#     MODERATION = 2
#     PUBLISHED = 3

# class UserRoles(Enum): 
#     READER = 1
#     EDITOR = 2
#     ADMIN = 3


# class Document: 
#     def __init__(self, state: DocumentState, current_user_role: UserRoles):
#         self.state = state
#         self.current_user_role = current_user_role

#     def publish(self): 

#         if self.state == DocumentState.DRAFT: 
#             self.state = DocumentState.MODERATION

#         elif self.state == DocumentState.MODERATION and self.current_user_role == UserRoles.ADMIN: 
#             self.state = DocumentState.PUBLISHED


# d = Document(DocumentState.DRAFT, UserRoles.EDITOR)
# print(f"Inital", d.state.name)

# d.publish()
# print(f"Final", d.state.name)

# # Good Example

# from enum import Enum
# from abc import ABC, abstractmethod

# class UserRoles(Enum): 
#     READER = 1
#     EDITOR = 2
#     ADMIN = 3

# class State(ABC): 
#     @abstractmethod
#     def publish(self): 
#         pass 


# class DraftState(State): 
#     def __init__(self, document):
#         self._document = document

#     def publish(self):
#         self._document.state = ModerationState(self._document)


# class ModerationState(State): 
#     def __init__(self, document):
#         self._document = document

#     def publish(self):
#         if self._document.current_user_role == UserRoles.ADMIN: 
#             self._document.state = PublishState(self._document)

# class PublishState(State): 

#     def __init__(self, document):
#         self._document = document

#     def publish(self):
#         pass
        


# class Document: 
#     def __init__(self, current_user_role: UserRoles):
#         self.state = DraftState(self)
#         self.current_user_role = current_user_role

#     def publish(self): 
#         self.state.publish()


# d = Document(UserRoles.EDITOR)
# print(f"Inital", d.state.__class__.__name__)

# d.publish()
# print(f"Final", d.state.__class__.__name__)

# d.current_user_role = UserRoles.ADMIN
# d.publish()
# print(f"Final", d.state.__class__.__name__)

# ==================================

# # Observer Pattern 

# # Bad example 

# class Sheet2: 
#     def __init__(self):
#         self.total = 0 

#     def calculate_total(self, values: list[float]): 
#         sum = 0
#         for value in values: 
#             sum += value 
#         self.total = sum 
#         print("total", self.total)
#         return self.total
    
# class BarChart: 
#     def render(self, values: list[float]): 
#         print("Rendering")

# class DataSource: 
#     def __init__(self):
#         self._values: list[float] = []
#         self.dependents: list[object] = []

#     @property
#     def values(self) -> list[float]: 
#         return self._values
    
#     @values.setter      # The getter @property needs to exists for this to work
#     def values(self, values:list[float]) -> None: 
#         self._values = values
        
#         for dependent in self.dependents: 
#             if isinstance(dependent, Sheet2): 
#                 dependent.calculate_total(values)
#             elif isinstance(dependent, BarChart): 
#                 dependent.render(values)

#     def add_dependents(self, dependent: object): 
#         self.dependents.append(dependent)

#     def remove_dependents(self, dependent: object): 
#         self.dependents.remove(dependent)

# sheet2 = Sheet2()
# barChart = BarChart()

# data_source = DataSource()
# data_source.add_dependents(barChart)
# data_source.add_dependents(sheet2)

# data_source.values = [1,2,3,4.1]

# print("removing bar chart")
# data_source.remove_dependents(barChart)
# data_source.values = [10,1]

# # Good example 

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self): 
        pass

class Sheet2(Observer): 
    def __init__(self, data_source):
        self.total = 0
        self.data_source = data_source 

    def update(self): 
        self.calculate_total(self.data_source.values)

    def calculate_total(self, values: list[float]): 
        sum = 0
        for value in values: 
            sum += value 
        self.total = sum 
        print("total", self.total)
        return self.total
    
class BarChart(Observer): 
    def __init__(self, data_source):
        self.data_source = data_source 

    def update(self): 
        print("Rendering")

class Subject: # Observer manager 
    def __init__(self):
        self.observers: list[Observer] = []

    def add_observer(self, observer: Observer): 
        self.observers.append(observer)

    def remove_observer(self, observer: Observer): 
        self.observers.remove(observer)
    
    def notify_observer(self): 
        for observer in self.observers:
            observer.update()


class DataSource(Subject): 
    def __init__(self):
        super().__init__()
        self.values: list[float] = []

    @property
    def values(self) -> list[float]: 
        return self._values
    
    @values.setter      # The getter @property needs to exists for this to work
    def values(self, values:list[float]) -> None: 
        self._values = values
        super().notify_observer()

data_source = DataSource()

sheet2 = Sheet2(data_source)

bar_chart = BarChart(data_source)
   
data_source.add_observer(bar_chart)
data_source.add_observer(sheet2)

print(data_source.values)

data_source.values = [1,2,3,4]