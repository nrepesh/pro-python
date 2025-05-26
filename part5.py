# State Pattern 

# Bad Example 

from enum import Enum 

class DocumentState(Enum): 
    DRAFT = 1
    MODERATION = 2
    PUBLISHED = 3

class UserRoles(Enum): 
    READER = 1
    EDITOR = 2
    ADMIN = 3


class Document: 
    def __init__(self, state: DocumentState, current_user_role: UserRoles):
        self.state = state
        self.current_user_role = current_user_role

    def publish(self): 

        if self.state == DocumentState.DRAFT: 
            self.state = DocumentState.MODERATION

        elif self.state == DocumentState.MODERATION and self.current_user_role == UserRoles.ADMIN: 
            self.state = DocumentState.PUBLISHED


d = Document(DocumentState.DRAFT, UserRoles.EDITOR)
print(f"Inital", d.state.name)

d.publish()
print(f"Final", d.state.name)

# Good Example

from enum import Enum
from abc import ABC, abstractmethod

class UserRoles(Enum): 
    READER = 1
    EDITOR = 2
    ADMIN = 3

class State(ABC): 
    @abstractmethod
    def publish(self): 
        pass 


class DraftState(State): 
    def __init__(self, document):
        self._document = document

    def publish(self):
        self._document.state = ModerationState(self._document)


class ModerationState(State): 
    def __init__(self, document):
        self._document = document

    def publish(self):
        if self._document.current_user_role == UserRoles.ADMIN: 
            self._document.state = PublishState(self._document)

class PublishState(State): 

    def __init__(self, document):
        self._document = document

    def publish(self):
        pass
        


class Document: 
    def __init__(self, current_user_role: UserRoles):
        self.state = DraftState(self)
        self.current_user_role = current_user_role

    def publish(self): 
        self.state.publish()


d = Document(UserRoles.EDITOR)
print(f"Inital", d.state.__class__.__name__)

d.publish()
print(f"Final", d.state.__class__.__name__)

d.current_user_role = UserRoles.ADMIN
d.publish()
print(f"Final", d.state.__class__.__name__)

# ==================================

# Observer Pattern 

# Bad example 

class Sheet2: 
    def __init__(self):
        self.total = 0 

    def calculate_total(self, values: list[float]): 
        sum = 0
        for value in values: 
            sum += value 
        self.total = sum 
        print("total", self.total)
        return self.total
    
class BarChart: 
    def render(self, values: list[float]): 
        print("Rendering")

class DataSource: 
    def __init__(self):
        self._values: list[float] = []
        self.dependents: list[object] = []

    @property
    def values(self) -> list[float]: 
        return self._values
    
    @values.setter      # The getter @property needs to exists for this to work
    def values(self, values:list[float]) -> None: 
        self._values = values
        
        for dependent in self.dependents: 
            if isinstance(dependent, Sheet2): 
                dependent.calculate_total(values)
            elif isinstance(dependent, BarChart): 
                dependent.render(values)

    def add_dependents(self, dependent: object): 
        self.dependents.append(dependent)

    def remove_dependents(self, dependent: object): 
        self.dependents.remove(dependent)

sheet2 = Sheet2()
barChart = BarChart()

data_source = DataSource()
data_source.add_dependents(barChart)
data_source.add_dependents(sheet2)

data_source.values = [1,2,3,4.1]

print("removing bar chart")
data_source.remove_dependents(barChart)
data_source.values = [10,1]

# Good example 

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

# =====================================================

# Facade Pattern 

# Bad example fixed to good

class OrderRequest: 
    def __init__(self):
        self.name = "dan"
        self.card_number = "123"
        self.amount = "20.99"
        self.address = "123 Texas"
        self.item_ids = ["123", "423", "555", "989"]

class Authenticator: 
    def authenticate(self)->bool: 
        return True 
    
class Inventory: 
    def check_inventory(self, item_id:str) -> bool: 
        return True 
    
    def reduce_inventory(self, item_id: str, amount: int): 
        print(f"Simulating database remove of {item_id} by {amount}")

class Payment: 
    def __init__(self,name, card_number, amount):
        self._name = name 
        self._card_number = card_number
        self._amount = amount 

    def pay(self): 
        print(f"Charging card of {self._name}")

class OrderFullfilment: 
    def __init__(self, inventory: Inventory):
        self._inventory = inventory 

    def fulfil(self, name, address, items): 
        print("Insert to DB ")
        for item in items: 
            self._inventory.reduce_inventory(item, 1)

class OrderService: 
    def create(self, order_req: OrderRequest): 
        auth = Authenticator()
        auth.authenticate()

        inventory = Inventory()
        for item_id in order_req.item_ids:
            inventory.check_inventory(item_id)

        payment = Payment(order_req.name, order_req.card_number, order_req.amount)
        payment.pay()

        order_fulfillment = OrderFullfilment(inventory)
        order_fulfillment.fulfil(order_req.name, order_req.address, order_req.item_ids)


order_req = OrderRequest()
order_ser = OrderService()
order_ser.create(order_req)

 # ===========================================

# Adapter pattern 
# Bad example 
from abc import ABC, abstractmethod

class Video: 
    def play(self): 
        print("Playing video...")

    def stop(self): 
        print("Stopping Video...")

class Color(ABC): 
    @abstractmethod
    def apply(self, video): 
        pass 

# 3rd party library. Cannot change.
class Rainbow:
    def setup(self): 
        print("Setting rainbow filter")
    
    def update(self, video): 
        print("Apply rainbow")

class BlackAndWhiteColor(Color): 
    def apply(self, video): 
        print("B&W")

class MidnightColor(Color): 
    def apply(self, video): 
        print("Midnight")

class VideoEditor: 
    def __init__(self, video):
        self.video = video 

    def apply_color(self, color: Color): 
        color.apply(self.video)

video = Video()
video_editor = VideoEditor(video)

video_editor.apply_color(BlackAndWhiteColor())

# Good example 

from abc import ABC, abstractmethod

class Video: 
    def play(self): 
        print("Playing video...")

    def stop(self): 
        print("Stopping Video...")

class Color(ABC): 
    @abstractmethod
    def apply(self, video): 
        pass 

# 3rd party library. Cannot change.
class Rainbow:
    def setup(self): 
        print("Setting rainbow filter")
    
    def update(self, video): 
        print("Apply rainbow")

class RainbowColor(Color): 
    def __init__(self, rainbow: Rainbow):
        self._rainbow = rainbow

    def apply(self, video):
        self._rainbow.setup()
        self._rainbow.update(video)
        

class BlackAndWhiteColor(Color): 
    def apply(self, video): 
        print("B&W")

class MidnightColor(Color): 
    def apply(self, video): 
        print("Midnight")

class VideoEditor: 
    def __init__(self, video):
        self.video = video 

    def apply_color(self, color: Color): 
        color.apply(self.video)

video = Video()
video_editor = VideoEditor(video)

video_editor.apply_color(BlackAndWhiteColor())
video_editor.apply_color(RainbowColor(Rainbow()))


# ================================== 

# Prototype pattern. 

# Bad example

from abc import ABC, abstractmethod

class Shape(ABC): 
    @abstractmethod
    def draw(self): 
        pass 

class Circle(Shape): 
    def __init__(self):
        self.radius = 5

    def draw(self):
        print(f"Drawing circle with radius {self.radius}")

class Rectangle(Shape): 
    def __init__(self):
        self.width = 10 
        self.height = 5

    def draw(self):
        print(f"Drawing rect with width {self.width} and height {self.height}")

class ShapeActions: 
    def duplicate(self, shape: Shape): 
        if isinstance(shape, Circle): 
            new_circle = Circle()
            new_circle.radius = shape.radius
            new_circle.draw()
        elif isinstance(shape, Rectangle): 
            new_rect = Rectangle()
            new_rect.width = shape.width
            new_rect.height = shape.height
            new_rect.draw()
        else: 
            raise ValueError("Invalid shape")


c1 = Circle()
c1.draw()
c1.radius = 12
c1.draw()

r1 = Rectangle()
r1.draw()
r1.height = 12
r1.width = 20
r1.draw()

shape_actions = ShapeActions()
shape_actions.duplicate(c1)
shape_actions.duplicate(r1)

# Good example 

from abc import ABC, abstractmethod

class Shape(ABC): 
    @abstractmethod
    def draw(self): 
        pass 
    
    @abstractmethod
    def duplicate(self) -> 'Shape': 
        pass

class Circle(Shape): 
    def __init__(self, radius):
        self.radius = radius

    def draw(self):
        print(f"Drawing circle with radius {self.radius}")

    def duplicate(self):
        new_circle = Circle(self.radius)
        return new_circle

        

class Rectangle(Shape): 
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self):
        print(f"Drawing rect with width {self.width} and height {self.height}")

    def duplicate(self):
        new_rectangle = Rectangle(self.width, self.height)
        return new_rectangle

class ShapeActions: 
    def duplicate(self, shape: Shape): 
        new_shape = shape.duplicate()
        new_shape.draw()


shape_actions = ShapeActions()

circle = Circle(5)
circle.draw()

rect = Rectangle(5,10)
rect.draw()

shape_actions.duplicate(circle)
shape_actions.duplicate(rect)

# =====================================

# Abstact factory Pattern

# Bad example 

from enum import Enum
from abc import ABC, abstractmethod

class OperatingSystemType(Enum): 
    Windows = "Windows"
    Mac = "Mac"

class UIComponent(ABC): 
    @abstractmethod
    def render(self): 
        pass 

class Checkbox(UIComponent): 
    @abstractmethod
    def on_select(self): 
        pass 

class Button(UIComponent): 
    @abstractmethod
    def on_click(self): 
        pass 


class WindowsButton(Button): 
    def render(self): 
        print("Windows render button")

    def on_click(self):
        print("Window button clicked")

class WindowsCheckBox(Checkbox):
    def render(self):
        print("Windows render checkbox")

    def on_select(self):
        print("Windows checkbox selected")

class MacButton(Button): 
    def render(self): 
        print("mac render button")

    def on_click(self):
        print("mac button clicked")

class MacCheckBox(Checkbox):
    def render(self):
        print("mac render checkbox")

    def on_select(self):
        print("mac checkbox selected")


# Application code 
class UserSettingsForm: 
    def render(self, os: OperatingSystemType): 
        if os == OperatingSystemType.Windows: 
            WindowsButton().render()
            WindowsCheckBox().render()
        elif os == OperatingSystemType.Mac: 
            MacButton().render()
            MacCheckBox().render()

os = OperatingSystemType.Windows
user_setting_form = UserSettingsForm()
user_setting_form.render(os)

# Good example: 

from enum import Enum
from abc import ABC, abstractmethod

class OperatingSystemType(Enum): 
    Windows = "Windows"
    Mac = "Mac"

class UIComponent(ABC): 
    @abstractmethod
    def render(self): 
        pass 

class Checkbox(UIComponent): 
    @abstractmethod
    def on_select(self): 
        pass 

class Button(UIComponent): 
    @abstractmethod
    def on_click(self): 
        pass 

class UIComponentFactory(ABC): 
    @abstractmethod
    def create_button(self) -> Button: 
        pass 

    @abstractmethod
    def create_checkbox(self) -> Checkbox: 
        pass 

class WindowsUIComponentFactory(UIComponentFactory): 
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckBox()
    
class MacUIComponentFactory(UIComponentFactory): 
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckBox()
    



class WindowsButton(Button): 
    def render(self): 
        print("Windows render button")

    def on_click(self):
        print("Window button clicked")

class WindowsCheckBox(Checkbox):
    def render(self):
        print("Windows render checkbox")

    def on_select(self):
        print("Windows checkbox selected")

class MacButton(Button): 
    def render(self): 
        print("mac render button")

    def on_click(self):
        print("mac button clicked")

class MacCheckBox(Checkbox):
    def render(self):
        print("mac render checkbox")

    def on_select(self):
        print("mac checkbox selected")


# Application code 
class UserSettingsForm: 
    def render(self,ui_component_factory: UIComponentFactory): 
        ui_component_factory.create_button().render()
        ui_component_factory.create_checkbox().render()

os = OperatingSystemType.Windows
ui_component_factory: UIComponentFactory

if os == OperatingSystemType.Windows: 
    ui_component_factory = WindowsUIComponentFactory()
elif os == OperatingSystemType.Mac: 
    ui_component_factory = MacUIComponentFactory()

user_setting_form = UserSettingsForm()
user_setting_form.render(ui_component_factory)
