import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.coordinates = []

    def place_ship(self, start_x, start_y, direction):
        if direction == 'horizontal':
            self.coordinates = [(start_x + i, start_y) for i in range(self.size)]
        elif direction == 'vertical':
            self.coordinates = [(start_x, start_y + i) for i in range(self.size)]

class GameBoard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_board = [[" " for _ in range(10)] for _ in range(10)]
        self.ai_board = [[" " for _ in range(10)] for _ in range(10)]
        self.ships = {1: 4, 2: 3, 3: 2, 4: 1}

    def generate_ships(self, board):
        ships_info = [(4, 1), (3, 2), (2, 3), (1, 4)]

        for size, count in ships_info:
            for _ in range(count):
                ship_instance = Ship(size=size)
                self.place_ships(size, ship_instance, board)

    def place_ships(self, size, ship, board):
        max_attempts = 100
        margin = 1

        placed = False
        for _ in range(max_attempts):
            direction = random.choice(['horizontal', 'vertical'])

            if direction == 'horizontal':
                start_x = random.randint(0, self.x - ship.size)
                start_y = random.randint(0, self.y - 1)
            else:
                start_x = random.randint(0, self.x - 1)
                start_y = random.randint(0, self.y - ship.size)

            ship.place_ship(start_x, start_y, direction)

            if not self.check_collision(ship, margin, board):
                for x, y in ship.coordinates:
                    board[x][y] = "#"

                if size in self.ships:
                    self.ships[size] -= 1

                    if self.ships[size] == 0:
                        del self.ships[size]

                placed = True
                break
            else:
                margin += 1

        if not placed:
            self.place_ships(size, ship, board)

    def check_collision(self, ship, margin, board):
        for coord in ship.coordinates:
            for x_offset in range(-margin, ship.size + margin):
                for y_offset in range(-margin, margin + 1):
                    x = coord[0] + x_offset
                    y = coord[1] + y_offset

                    if not (0 <= x < self.x and 0 <= y < self.y):
                        continue

                    if board[x][y] == "#":
                        return True

        return False

    def generate_player_board(self):
        self.generate_ships(self.player_board)

    def generate_ai_board(self):
        self.generate_ships(self.ai_board)

    def display_player_board(self):
        print("\nИгровое поле игрока:")
        print("   0  1  2  3  4  5  6  7  8  9")
        print("  -----------------------------")
        for i in range(10):
            print(f"{i}|", end='')
            for j in range(10):
                print(f" {self.player_board[i][j]}", end=' ')
            print("|")
        print("  -----------------------------")

    def display_ai_board(self):
        print("\nИгровое поле ИИ:")
        print("   0  1  2  3  4  5  6  7  8  9")
        print("  -----------------------------")
        for i in range(10):
            print(f"{i}|", end=' ')
            for j in range(10):
                if self.ai_board[i][j] == "#":
                    print(" ", end='  ')
                else:
                    print(f"{self.ai_board[i][j]}", end='  ')
            print("|")
        print("  -----------------------------")

class Player:
    def __init__(self, game_board):
        self.game_board = game_board

    def shoot_at_ai_board(self):
        while True:
            try:
                target_x = int(input("Введите координату X (от 0 до 9): "))
                target_y = int(input("Введите координату Y (от 0 до 9): "))

                if not (0 <= target_x <= 9 and 0 <= target_y <= 9):
                    print("Координаты выходят за границы поля. Попробуйте снова.")
                    continue

                if self.game_board.ai_board[target_x][target_y] == "*" or self.game_board.ai_board[target_x][target_y] == "-":
                    print("Вы уже стреляли в эти координаты. Попробуйте снова.")
                    continue

                if self.game_board.ai_board[target_x][target_y] == "#":
                    print(f"Координаты: ({target_x}, {target_y})")
                    self.game_board.ai_board[target_x][target_y] = "*"
                    self.game_board.display_ai_board()
                    return True
                else:
                    print(f"Координаты: ({target_x}, {target_y})")
                    self.game_board.ai_board[target_x][target_y] = "-"
                    self.game_board.display_ai_board()
                    return False

            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
            except IndexError:
                print("Некорректные координаты. Попробуйте снова.")
            else:
                break
        return False

class AIPlayer:
    def __init__(self, game_board):
        self.game_board = game_board

    def shoot_at_player_board(self):
        while True:
            target_x = random.randint(0, 9)
            target_y = random.randint(0, 9)

            if self.game_board.player_board[target_x][target_y] == "*" or self.game_board.player_board[target_x][target_y] == "-":
                continue

            if self.game_board.player_board[target_x][target_y] == "#":
                print(f"Координаты: ({target_x}, {target_y})")
                self.game_board.player_board[target_x][target_y] = "*"
                self.game_board.display_player_board()
                return True
            else:
                print(f"Координаты: ({target_x}, {target_y})")
                self.game_board.player_board[target_x][target_y] = "-"
                self.game_board.display_player_board()
                return False

class VictoryConditions:
    def is_winner(self, player):
        for row in player.game_board.ai_board:
            if "#" in row:
                return False
        return True

class Game:
    def __init__(self, player, ai_player):
        self.player = player
        self.ai_player = ai_player
        self.victory_conditions = VictoryConditions()
        self.game_board = GameBoard(10, 10)

    def play(self):
        while True:
            print("Ход игрока:")
            continue_shooting = True

            while continue_shooting:
                if self.player.shoot_at_ai_board():
                    print("Попадание! Ходите снова.")
                else:
                    print("Промах! Ход ИИ.")
                    continue_shooting = False

                if self.victory_conditions.is_winner(self.ai_player):
                    return "ai"

            print("Ход ИИ:")
            if self.ai_player.shoot_at_player_board():
                print("Попадание! Ход ИИ снова.")
            else:
                print("Промах! Ход игрока.")

            if self.victory_conditions.is_winner(self.player):
                return "player"


game_board_instance = GameBoard(10, 10)
player_instance = Player(game_board_instance)
ai_player_instance = AIPlayer(game_board_instance)

game_board_instance.generate_player_board()
game_board_instance.generate_ai_board()

game_board_instance.display_player_board()
game_board_instance.display_ai_board()

game_instance = Game(player_instance, ai_player_instance)

while True:
    result = game_instance.play()

    if result == "player":
        print("ИИ победил!")
    elif result == "ai":
        print("Игрок победил!")

    choice = input("Хотите сыграть еще раз? (1 - да, 2 - нет): ")
    if choice == "2":
        print("Спасибо за игру! До свидания.")
        break
    elif choice == "1":
        game_board_instance = GameBoard(10, 10)
        player_instance = Player(game_board_instance)
        ai_player_instance = AIPlayer(game_board_instance)

        game_board_instance.generate_player_board()
        game_board_instance.generate_ai_board()

        game_board_instance.display_player_board()
        game_board_instance.display_ai_board()

        game_instance.player = player_instance
        game_instance.ai_player = ai_player_instance