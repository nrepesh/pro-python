# Single Responsibility Principle(SRP)

class EmailSender: 

    def send(self, recipient, message): 
        print("Sending email", recipient, message)

class User: 
    def __init__(self, username, email): 
        # This might change the class cause new data might be added. 
        self.username = username 
        self.email = email 

    def register(self): 
        # This might change the class cause the downstream might change. 
        print(f"Registering user {self.username}")

        email_sender = EmailSender()
        email_sender.send(self.email, f"Welcome {self.username}")

user = User("dantheman", "dan@gmail.com")
user.register()

# =======================================

class EmailSender: 

    def send(self, recipient, message): 
        print("Sending email", recipient, message)

class User: 
    def __init__(self, username, email): 
        self.username = username 
        self.email = email 

class UserService: 
    def register(self, user): 
        print(f"Registering user {user.username}")

        email_sender = EmailSender()
        email_sender.send(user.email, f"Welcome {user.username}")

    def update(self, user): 
        print("updating", user.username)

    def delete(self, user): 
        print("updating", user.username)

user = User("dantheman", "dan@gmail.com")
user_service = UserService()
user_service.register(user)

# =======================================
# Using composition

class EmailSender: 

    def send(self, recipient, message): 
        print("Sending email", recipient, message)

class User: 
    def __init__(self, username, email): 
        self.username = username 
        self.email = email 

class UserService: 

    def __init__(self, user: User):
        self.user = user

    def register(self): 
        print(f"Registering user {self.user.username}")

        email_sender = EmailSender()
        email_sender.send(user.email, f"Welcome {self.user.username}")

    def update(self): 
        print("updating", self.user.username)

    def delete(self): 
        print("updating", self.user.username)

user = User("dantheman", "dan@gmail.com")
user_service = UserService(user)
user_service.register()

user2 = User("joe", "joe@gmail.com")
user_service2 = UserService(user2)
user_service2.register()

# =======================================

# Bad Open/Close Principle (OCP)

from enum import Enum
import math 

class ShapeType(Enum): 
    CIRCLE = 'circle'
    RECTANGLE = 'rectangle'


class Shape: 
    def __init__(self, shape_type: ShapeType, radius: float = 0, height: float = 0, width: float = 0): 
        self.type = shape_type
        self.radius = radius 
        self.height = height 
        self.width = width 

    def calculate_area(self) -> float: 
        if self.type == ShapeType.CIRCLE: 
            return math.pi*self.radius**2
        elif self.type == ShapeType.RECTANGLE: 
            return self.height * self.width
        else: 
            raise ValueError("Unsupported Shape Type")
        
circle = Shape(ShapeType.CIRCLE, radius=5)
rect = Shape(ShapeType.RECTANGLE, height=4, width=6)

print("circle", circle.calculate_area())
print("rect", rect.calculate_area())

# =======================================

 # Good Open/Close Principle (OCP)

from enum import Enum
import math 
from abc import ABC, abstractmethod

class Shape(ABC): 
    @abstractmethod
    def calculate_area(self) -> float: 
        pass

# Using Inheritance 
class Circle(Shape): 
    def __init__(self, radius): 
        self.radius = radius

    # Using polymorphism
    def calculate_area(self):
        return math.pi*self.radius**2
    

class Rectangle(Shape): 
    def __init__(self, height, width): 
        self.height = height
        self.width = width

    def calculate_area(self):
        return self.height * self.width
        
circle = Circle(radius=5)
rect = Rectangle(height=4, width=6)

print("circle", circle.calculate_area())
print("rect", rect.calculate_area())

# =======================================

 # Liskov substitution principle (LSP)

 # BAD example

from abc import ABC, abstractmethod

class Shape(ABC): 
    @abstractmethod
    def area(self)->float: 
        pass 

class Rectangle(Shape): 
    def __init__(self, height: float = 0.0, width: float = 0.0):
        self._height = height 
        self._width = width 

    @property
    def width(self)->float: 
        return self._width
    
    @width.setter
    def width(self, new_width: float):
        self._width = new_width

    @property
    def height(self)->float: 
        return self._height
    
    @height.setter
    def height(self, new_height: float):
        self._height = new_height

    def area(self)->float: 
        return self._width*self._height
    
class Square(Rectangle): 
    # The grandchild does not need to implement the abstract method
    def __init__(self, side:float = 0):
        super().__init__(side, side)

    @Rectangle.width.setter
    def width(self, value: float): 
        self._height = value 
        self._width = value 

    @Rectangle.height.setter
    def height(self, value: float): 
        self._width = value 
        self._height = value


rect = Rectangle()
rect.width = 5
rect.height = 10 
print("expected = 50, actual", rect.area())

rect = Square()
rect.width = 5
rect.height = 10 
print("expected = 50, actual", rect.area())


# Good example

from abc import ABC, abstractmethod

class Shape(ABC): 
    @abstractmethod
    def area(self)->float: 
        pass 

class Rectangle(Shape): 
    def __init__(self, height: float = 0.0, width: float = 0.0):
        self.height = height 
        self.width = width 

    def area(self)->float: 
        return self.width*self.height
    
class Square(Shape): 
    def __init__(self, side:float = 0):
        self.side = side 

    def area(self): 
        return self.side * self.side

    
rect = Rectangle()
rect.width = 5
rect.height = 10 
print("expected = 50, actual", rect.area())

sq = Square()
sq.side = 5
print("expected = 25, actual", sq.area())

def return_area(shape: Shape): 
    return shape.area()

print("rect", return_area(rect))
print("sq", return_area(sq))


# =========================================

# Interface Segregation Principle (ISP)

# Bad example 

from abc import ABC, abstractmethod
import math

class shape(ABC): 
    @abstractmethod
    def area(self): 
        pass 

    @abstractmethod
    def volume(self): 
        pass

class Circle(shape): 
    def __init__(self, radius:float = 0.0):
        self.radius = radius

    def area(self):
        return math.pi*self.radius**2
    
    def voulme(self): 
        raise NotImplementedError("Volume not applicable for 2D shapes.")
    
class Sphere(shape): 
    def __init__(self, radius:float = 0.0):
        self.radius = radius 

    def area(self):
        return 4*math.pi*self.radius**2
    
    def voulme(self): 
        return (4/3)*math.pi*self.radius**3

circle = Circle(5)
sphere = Sphere(5)

# Good example

from abc import ABC, abstractmethod
import math

class shape3d(ABC): 
    @abstractmethod
    def area(self): 
        pass 

    @abstractmethod
    def volume(self): 
        pass

class shape2d(ABC): 
    @abstractmethod
    def area(self): 
        pass

class Circle(shape2d): 
    def __init__(self, radius:float = 0.0):
        self.radius = radius

    def area(self):
        return math.pi*self.radius**2
    
class Sphere(shape3d): 
    def __init__(self, radius:float = 0.0):
        self.radius = radius 

    def area(self):
        return 4*math.pi*self.radius**2
    
    def voulme(self): 
        return (4/3)*math.pi*self.radius**3

circle = Circle(5)
sphere = Sphere(5)

# =======================

# Dependency Inversion Principle (DIP)

# Bad example 

class Engine: 
    def start(self): 
        print("Engine started")

class Car: 
    def __init__(self):
        self.engine = Engine() # Violates open-close principle. If you wanted to give a fast engine.

    def start(self): 
        self.engine.start()
        print("car started")


c = Car()
c.start()

# Good example 

from abc import ABC, abstractmethod

class Engine(ABC): 

    @abstractmethod
    def start(self): 
        pass


class BasicEngine(Engine): 
    def start(self): 
        print("Basic engine started")
    
class FastEngine(Engine): 
    def start(self): 
        print("Fast engine started")


class Car: 
    def __init__(self, engine: Engine):
        self.engine = engine

    def start(self): 
        self.engine.start()
        print("Car started")


fastEngine = FastEngine()
c = Car(fastEngine)
c.start()
