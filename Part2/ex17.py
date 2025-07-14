import random

#Get name
name = input("What is your name?\n")
#List adjective
adjective = ["Tung Tung Tung Tung Tung Tung Tung", "Bombardino", "Cappuccino", "Tralalero", "Bombombini", "Chimpazini"]
brainrot = ["Assassino", "Tralala", "Crocodilo", "Sahur", "Gusini", "Bananini"]

user = random.choice(adjective) + " " + random.choice(brainrot)
print(f"{name}, your code name is : {user}")
print(f"Your lucky number is:  {random.randint(0,99)}")

