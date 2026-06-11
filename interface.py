import logic as lbb
import objects as obb
import random 



def main_menu():
    print ("""
    === BOMBERMAN ===
    1. New game
    2. load game
    3. delete game
    4. exit game
    """)
    option = input ("select an option: ")
    
    return option

def main():
    option = main_menu()
    save = None

    if option == "4":
        print("Game over")
        return None

    elif option == "3":
        username = input("Put your username: ")
        saves = lbb.list_user_saves(username)

        if not saves:
            print("No game is saved")
            return None

        print("Games found:")
        for i, file in enumerate(saves):
            print(f"{i + 1}. {file}")

        selected = int(input("Seleccione cuál eliminar: ")) - 1

        if selected < 0 or selected >= len(saves):
            print("Invalid selection")
            return None

        lbb.delete_save(saves[selected])
        print("Game deleted")
        return None

    elif option == "2":
        username = input("Put your username: ")
        save_file = lbb.list_user_saves(username)

        if not save_file:
            print("No saved games")
            return None

        print("Games found:")
        for i, file in enumerate(save_file):
            print(f"{i + 1}. {file}")

        selected = int(input("Select the number of the game: ")) - 1

        if selected < 0 or selected >= len(save_file):
            print("Invalid selection")
            return None

        selected_save = save_file[selected]
        save = lbb.load_specific_save(selected_save)

        level = save["level"]
        rows = save["rows"]
        cols = save["cols"]
        world = save["world"]
        pos = tuple(save["player_pos"])

        print(f"Loading level {level} for user {username}...")

    elif option == "1":
        username = input("Put your username: ")
        level = 1
        print(f"Starting new game for user {username}...")

    else:
        print("Invalid option")
        return None

    while level <= 3:

        if save:
            print(f"Loading saved level {level}...")
            save = None

        else:
            print(f"Loading level {level}...")

            rows = random.randint(8, 15)
            cols = random.randint(8, 15)

            world = lbb.establish_world(rows, cols)
            available_positions = lbb.available_positions(world, rows, cols)

            _, _, pos = lbb.add_player(world, available_positions)

            num_boxes = 8 + (level * 4)
            num_walls = 8 + (level * 4)
            num_enemies = 2 + level

            for __ in range(num_boxes):
                world, available_positions = lbb.add_boxes(world, available_positions)

            for __ in range(num_walls):
                world, available_positions = lbb.add_walls(world, available_positions)

            lbb.add_door(world, available_positions)

            for __ in range(num_enemies):
                world, available_positions = lbb.add_enemies(world, available_positions)

        result, pos = lbb.move_player(world, pos, rows, cols)

        if result == "next_level":
            level += 1

            if level == 4:
                print("You won the game!")
                return None

            print(f"You pass to level {level}")

        elif result == "you_died":
            print("Game over")
            return None

        elif result == "exit":
            lbb.save_game(username, level, world, pos, rows, cols)
            print("The game was saved...")
            return None
        

main ()