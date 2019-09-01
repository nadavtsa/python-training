import random
import hello_worls
health = 50
difficulty = random.randint(1, 3)
potion_health = int(random.randint(25, 50) / difficulty)
health = health + potion_health
print(health)
print(round(2.6))


