import datetime

class User: 
    def __init__(self, username, email, password): 
        self.username = username 
        self.__email = email       # Fully private variables. Cant access it outside. 
        self.password = password 

    def get_email(self): 
        print(f" Email accessed at {datetime.datetime.now()}")
        return self.__email
    
    def set_email(self, new_email): 
        if "@" in new_email:
            self.__email = new_email
    
    def clean_email(self): 
        return self.__email.lower().strip()


u1 = User("lordking", " lordking@gmail.com ", "loki")
u2 = User("Batman", "bat@gmail.com", "Alfred")

# print(u1.clean_email())
# print(u1.__email)

print(u1.get_email())
u1.set_email("lordgmail.com")
print(u1.get_email())

# ========================

class User: 
    def __init__(self, username, email, password): 
        self.username = username 
        self.__email = email       # Fully private variables. Cant access it outside. 
        self.password = password 

    @property
    def email(self): 
        return self.__email
    
    @email.setter
    def email(self, new_email): 
        if "@" in new_email:
            self.__email = new_email
    

u1 = User("Loki", "thor@gmail.com", "123")
print(u1.email)
u1.email = "Hello"
print(u1.email)
u1.email = "llookkii@gmail.com"
print(u1.email)

# =============================================

class User: 
    user_count = 0 

    def __init__(self, username, email): 
        self.username = username 
        self.email = email 
        User.user_count += 1

    def display_user(self): 
        print(f"Username: {self.username}, Email: {self.email}")

u1 = User("lordking", " lordking@gmail.com")
u2 = User("Batman", "bat@gmail.com")

print(User.user_count)
print(u1.user_count)

# ==============================

class BankAccount: 
    MIN_BALANCE = 100 

    def __init__(self, owner, balance = 0): 
        self.owner = owner 
        self._balance = balance 

    def deposit(self, amount): 
        if self._is_valid_amount(amount): 
            self._balance += amount 
            #print(f"{self.owner}'s new balance: ${self._balance}")
            self.__log_transaction("deposit", amount)
        else: 
            print("Deposit cannot be negative.")

    def _is_valid_amount(self, amount): 
        return amount > 0
    
    def __log_transaction(self, transaction_type, amount): 
        print(f"logging {transaction_type} of ${amount}. New balance: ${self._balance}")

    @staticmethod 
    def is_valid_interest_rate(rate): 
        return 0 <= rate <= 5
    

account = BankAccount("Alice", 500)
account.deposit(200)

account._is_valid_amount(200)
account.__log_transaction("deposit", 100000)

print(BankAccount.is_valid_interest_rate(3))
print(BankAccount.is_valid_interest_rate(10))