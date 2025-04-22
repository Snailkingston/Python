import random
import json
import os

# File to store the leaderboard
LEADERBOARD_FILE = "leaderboard.json"

# Load the leaderboard from a file
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Error loading leaderboard file. Starting with an empty leaderboard.")
            return []
    return []

# Save the leaderboard to a file
def save_leaderboard(leaderboard):
    try:
        with open(LEADERBOARD_FILE, "w") as file:
            json.dump(leaderboard, file, indent=4)
    except IOError:
        print("Error saving leaderboard to file.")

# Display the leaderboard
def display_leaderboard(leaderboard):
    print("\n===== Leaderboard =====")
    if not leaderboard:
        print("No scores yet. Play a game to make it to the leaderboard!")
    else:
        print(f"{'Rank':<5} {'Player':<15} {'Difficulty':<10} {'Score':<5}")
        for rank, entry in enumerate(leaderboard, start=1):
            print(f"{rank:<5} {entry['player']:<15} {entry['difficulty']:<10} {entry['score']:<5}")
    print("=======================\n")

# Update the leaderboard
def update_leaderboard(leaderboard, player_name, difficulty, score):
    # Add the new score to the leaderboard
    leaderboard.append({"player": player_name, "difficulty": difficulty, "score": score})
    # Sort the leaderboard by score in descending order
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    # Keep only the top 5 scores
    if len(leaderboard) > 5:
        leaderboard.pop()
    # Save the updated leaderboard to a file
    save_leaderboard(leaderboard)

# Play the number guessing game
def play_game(leaderboard):
    print("Welcome to the Number Guessing Game!")

    # Ask the user to enter their name
    player_name = input("Enter your name: ").strip()

    # Ask the user to select a difficulty level
    print("\nChoose a difficulty level:")
    print("1. Easy (Range: 1 to 100, 15 attempts)")
    print("2. Medium (Range: 1 to 500, 10 attempts)")
    print("3. Hard (Range: 1 to 1000, 5 attempts)")

    while True:
        difficulty = input("Enter your choice (1, 2, or 3): ").strip()
        if difficulty == "1":
            max_attempts = 15
            start_range, end_range = 1, 100
            difficulty_label = "Easy"
            print("You selected Easy difficulty. You have 15 attempts to guess a number between 1 and 100.")
            break
        elif difficulty == "2":
            max_attempts = 10
            start_range, end_range = 1, 500
            difficulty_label = "Medium"
            print("You selected Medium difficulty. You have 10 attempts to guess a number between 1 and 500.")
            break
        elif difficulty == "3" or difficulty == "":
            max_attempts = 5
            start_range, end_range = 1, 1000
            difficulty_label = "Hard"
            print("You selected Hard difficulty. You have 5 attempts to guess a number between 1 and 1000.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    # Generate a random number within the difficulty range
    random_number = random.randint(start_range, end_range)

    # Initialize attempts and score
    attempts = 0
    score = 0

    print("\nThe game has started! Good luck!")

    # Start the guessing loop
    while attempts < max_attempts:
        attempts += 1
        try:
            user_guess = int(input(f"Attempt {attempts}/{max_attempts}: Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            attempts -= 1  # Invalid input does not count as an attempt
            continue

        # Provide feedback on the user's guess
        if user_guess < random_number:
            print("Too low!")
        elif user_guess > random_number:
            print("Too high!")
        else:
            # If the guess is correct, calculate the score and break the loop
            if attempts == 1:
                score = 10
            elif attempts <= max_attempts // 2:
                score = 7
            else:
                score = 3
            print(f"Congratulations, {player_name}! You guessed the number in {attempts} attempts.")
            print(f"Your score: {score} points.")
            update_leaderboard(leaderboard, player_name, difficulty_label, score)  # Update leaderboard
            break

        # Give hints to the user
        if attempts < max_attempts:
            hint_even_odd = "even" if random_number % 2 == 0 else "odd"
            diff = abs(random_number - user_guess)
            hint_proximity = "close" if diff <= 10 else "far"
            print(f"Hint: The number is {hint_even_odd} and you are {hint_proximity} from the correct number.")

    else:
        # If the user exhausts all attempts, reveal the correct number
        print(f"Sorry, {player_name}, you've used all {max_attempts} attempts. The correct number was {random_number}.")
        print("Your score: 0 points.")
        update_leaderboard(leaderboard, player_name, difficulty_label, 0)  # Update leaderboard with 0 score

    # Display the updated leaderboard
    display_leaderboard(leaderboard)

# Main loop to allow the user to play again
def main():
    # Load the leaderboard from the file
    leaderboard = load_leaderboard()

    # Main game loop
    while True:
        display_leaderboard(leaderboard)  # Show leaderboard before each game
        play_game(leaderboard)
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thank you for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()

