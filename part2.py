
# Encapsulation 

class BadBankAccount: 
    def __init__(self, balance):
        self.balance = balance 



account = BadBankAccount(0.0)
account.balance = -1
print(account.balance)


class BankAccount: 
    def __init__(self, balance): 
        self._balance = balance


    @property
    def balance(self): 
        return self._balance
    
    # @balance.setter
    # def balance(self, new_balance): 
    #     self._balance = new_balance

    def deposit(self, amount):
        if amount <= 0: 
            raise ValueError("Deposit amount was negative")
        else: 
            self._balance += amount

    def withdraw(self, amount): 
        if amount <= 0: 
            raise ValueError("Withdraw amount was negative")
        if amount > self._balance: 
            raise ValueError("Insufficient Funds")
        else: 
            self._balance -= amount


account = BankAccount(0.0)
account.deposit(1.99)
print(account.balance)
account.withdraw(1)
print(account.balance)


# ===================

# Abstaction
# Reduce complexity by hiding unnecessary details. 

class EmailServices: 

    def _connect(self):
        print("Connecting to the email server")

    def _authenticate(self): 
        print("Authenticating...")

    def send_email(self): 
        self._connect()
        self._authenticate()
        print("Sending email...")
        self._disconnect()

    def _disconnect(self):
        print("Disconnect from email server...")


es = EmailServices()
es.send_email()


# ==========================

# Inheritance 

class Vehicle: 
    def __init__(self, brand:str, model:str, year:int):
        self.brand = brand 
        self.model = model 
        self.year = year 

    def start(self):
        print("Starting")

    def stop(self): 
        print("Stopping")


class Car(Vehicle): 

    def __init__(self, brand:str, model:str, year:int, num_doors:int, num_wheels:int): 
        super().__init__(brand, model, year)
        self.num_doors = num_doors
        self.num_wheels = num_wheels

class Bike(Vehicle):
    def __init__(self, brand:str, model:str, year:int, num_doors:int, num_wheels:int):
        super().__init__(brand, model, year)
        self.num_doors = num_doors
        self.num_wheels = num_wheels


c1 = Car("honda", "civic", "2025", "4", "4")
c1.start()

b1 = Bike("Honda", "R15", "2015", "2", "2")


# ==============================

# poly morphism 

class Vehicle: 
    def __init__(self, brand:str, model:str, year:int):
        self.brand = brand 
        self.model = model 
        self.year = year 

    def start(self):
        print("Starting")

    def stop(self): 
        print("Stopping")


class Car(Vehicle): 
    def __init__(self, brand:str, model:str, year:int, num_doors:int, num_wheels:int): 
        super().__init__(brand, model, year)
        self.num_doors = num_doors
        self.num_wheels = num_wheels

    def start(self):
        print("Car is starting")

class Bike(Vehicle):
    def __init__(self, brand:str, model:str, year:int, num_doors:int, num_wheels:int):
        super().__init__(brand, model, year)
        self.num_doors = num_doors
        self.num_wheels = num_wheels

    def start(self):
        print("Bike is starting")


vehicles = [
    Car("honda", "civic", "2025", "4", "4"),
    Bike("Honda", "R15", "2015", "2", "2")
]

for vehicle in vehicles:
    if isinstance(vehicle, Vehicle): 
        print(type(vehicle).__name__)
        vehicle.start()


# ================================================

# TIGHTLY COUPLED EXAMPLE 


class EmailSender: 
    def send(self, message): 
        print("Sending,", message)

class Order: 
    def create(self): 
        # Perform order creation logic, validate product stock
        email = EmailSender()
        email.send("Hi, your order was placed successfully.")

order = Order()
order.create()

# Refactoring to lowly coupled class

from abc import ABC, abstractmethod

class NotifcationService(ABC):
    @abstractmethod
    def send_notication(self, message: str): 
        pass

class EmailService(NotifcationService): 
    def send_notication(self, message): 
        print("Sending Email", message)

class MobileService(NotifcationService): 
    def send_notication(self, message):
        print("Sending SMS", message)

class Order: 
    def __init__(self, notification_service: NotifcationService):
        self.notification_service = notification_service

    def create(self): 
        self.notification_service.send_notication("Hi your order was placed.")

email = EmailService()
order = Order(email)
order.create()

# ================================================

# Composition 

class Engine: 
    def start(self): 
        print("Engine Starting")

class Wheels: 
    def rotate(self): 
        print("Rotate wheels")

class Chassis: 
    def support(self):
        print("Cassis supports")

class Seats: 
    def sit(self): 
        print("User can sit")


class Car: 

    def __init__(self):
        self._engine = Engine()
        self._wheels = Wheels()
        self._chassie = Chassis()
        self._seats = Seats()

    def start(self): 
        self._engine.start()
        self._wheels.rotate()
        self._chassie.support()
        self._seats.sit()
        print("CAR STARTED")


c1 = Car()
c1.start()