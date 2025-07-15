import random

# Computer picks a random number between 1 and 100
number_to_guess = random.randint(1, 100)
attempts = 0
max_attempts = 3

print("🎯 Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print(f"Max attempts : {max_attempts}")

while True:
    guess = input("Take a guess: ")

    if not guess.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess)
    attempts += 1

    if guess < number_to_guess:
        print("Too low. Try again!")
    elif guess > number_to_guess:
        print("Too high. Try again!")
    else:
        print(f"🎉 Congratulations! thats the right guess You guessed it in {attempts} attempts.")
        break
    
    print(f"Attempts left : {max_attempts - attempts}")
   
    if attempts == max_attempts:
        print(f"😢 Oops! You're out of attempts. The number was {number_to_guess}")
        break
