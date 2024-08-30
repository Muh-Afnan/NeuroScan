# class father:
#     def __init__(self):
#         self.property = "house"
#         print("father constructor is called")

#     def getEarning(self, var):
#         print(f"Father's get earning function is called at {var}")

#     def show(self):
#         print("I am being called")

# class son(father):
#     def __init__(self):
#         super().__init__()
#         super().getEarning("son")
#         self.vehicle = "BMW"
#         print("son constructor is called")

# class grandson(son):
#     def __init__(self):
#         super().__init__()
#         super().getEarning("grandson")
#         print("grandson constructor is called")
#         self.money = "500 Cr"
        

# Punit = grandson()
# Punit.show()
# print("file ran successfully")
# print(Punit.__dict__)

class father:
    def __init__(self):
        self.property = "house"
        print("father constructor is called")

    def getEarning(self, var):
        print(f"Father's get earning function is called at {var}")

    def show(self):
        print("I am being called")

class son():
    def __init__(self):
        self.vehicle = "BMW"
        print("son constructor is called")

class grandson(son, father):
    def __init__(self):
        super().__init__()
        super().getEarning("grandson")
        print("grandson constructor is called")
        self.money = "500 Cr"
        

Punit = grandson()
Punit.show()
print("file ran successfully")
print(Punit.__dict__)

