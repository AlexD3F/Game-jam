def main_menu():
    while True:
        print("Welcome to the Game Menu")
        print("1. Start Game")
        print("2. Load Game")
        print("3. Options")
        print("4. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            start_game()
        elif choice == '2':
            load_game()
        elif choice == '3':
            options()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def start_game():
    print("Starting the game...")
    # Your game logic goes here

def load_game():
    print("Loading the game...")
    # Your game loading logic goes here

def options():
    print("Options menu")
    # Your options menu logic goes here

if __name__ == "__main__":
    main_menu()