import os
import time
import random

board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
    [0, 4, 8], [2, 4, 6],             # Диагонали
]

scores = {"X": 0, "O": 0}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]}")
    print("-" * 11)
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("-" * 11)
    print(f" {board[6]} | {board[7]} | {board[8]}")

def is_cell_free(board, cell):
    return board[cell] not in ["X", "O"]


def player_input(board):
    while True:
        choice = input("\nВыберите ячейку (1-9): ")
        if choice.isdigit() and 1 <= int(choice) <= 9:
            cell = int(choice) - 1
            if is_cell_free(board, cell):
                return cell
            else:
                print("Ячейка занята. Выберите другую.")
        else:
            print("Некорректный ввод. Введите число от 1 до 9.")


def make_move(board, cell, player):
    board[cell] = player

# Функция на вход принимает значение текущего игрока (Х,О), а дальше меняет его на противоположное и возвращает
def switch_player(current_player):
    return "O" if current_player == "X" else "X"


# Функция проверяет есть ли выигрышные комбинации, на вход принимает основную переменную доски и значение последнего
# сходившего игрока (Х,О), а дальше смотрит по переменным списка WIN_COMBINATIONS, если все три ячейки
# совпадают со значением последнего сходившего игрока, то возвращает да - есть победитель, иначе нет
def check_winner(board, player):
    for combo in WIN_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


def check_draw(board):
    return all(cell in ["X", "O"] for cell in board)


# Функция печатает правила самой игры, реализована простыми операторами print
def show_instructions():
    print("\nДобро пожаловать в игру 'Крестики-Нолики'!")
    print("Правила:")
    print("- Игроки ходят по очереди, выбирая номер ячейки (1-9).")
    print("- Для победы нужно заполнить 3 клетки подряд (по горизонтали, вертикали или диагонали).")
    print("- Если поле заполнено и никто не победил — ничья.")
    print("- Удачи!")


def choose_game_mode():
    while True:
        # Функция strip() возвращает строку убирая лишние пробелы в начале и конце ввода, даже
        # если пользователь при вводе в начале или конце случайно ввел пробелы, то ошибки не будет
        mode = input("\nВыберите режим игры (1 — против другого игрока, 2 — против компьютера): ").strip()
        if mode in ["1", "2"]:
            return int(mode)
        else:
            print("Некорректный выбор. Введите 1 или 2.")


def computer_move(board):
    # Попробовать выиграть
    move = find_best_move(board, "O")
    if move is not None:
        return move

    # Блокировать игрока
    move = find_best_move(board, "X")
    if move is not None:
        return move

    # Случайный ход
    free_cells = [i for i in range(9) if is_cell_free(board, i)]
    return random.choice(free_cells)


def find_best_move(board, player):
    for combo in WIN_COMBINATIONS:
        cells = [board[i] for i in combo]
        if cells.count(player) == 2 and cells.count(" ") == 1:
            return combo[cells.index(" ")]
    return None

def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if is_cell_free(board, i):
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = str(i + 1)
            if score > best_score:
                best_score = score
                move = i
    return move

show_instructions()

while True:
    board = [" " for _ in range(9)]
    mode = choose_game_mode()
    if mode == 1:
        player_name_one = input("\nВведите имя первого игрока (X): ")
        print("Привет , " + player_name_one + "!")
        player_name_two = input("\nВведите имя второго игрока (O): ")
        print("Привет, " + player_name_two + "!")
        print("Игра начинается...")
        time.sleep(3)
    else:
        player_name_one = input("\nВведите имя игрока (X): ")
        print("Привет, " + player_name_one + "!")
        player_name_two = "Компьютер"
        print("Игра начинается...")
        time.sleep(3)
    current_player = random.choice(["X", "O"])
    if current_player == 'X':
        player_name = player_name_one
    else:
        player_name = player_name_two
    print(f"\nПервым ходит игрок {player_name}")
    input("\nНажмите Enter, чтобы начать...")

    for turn in range(9):  # Максимум 9 ходов
        clear_screen()
        show_instructions()
        print(f"\nСчёт: X - {scores['X']}, O - {scores['O']}")
        draw_board(board)
        if current_player == 'X':
            player_name = player_name_one
        else:
            player_name = player_name_two
        print(f"\nХод игрока {player_name}")
        if mode == 2 and current_player == "O":
            print("Компьютер думает...")
            cell = computer_move(board)
        else:
            cell = player_input(board)
        make_move(board, cell, current_player)
        if check_winner(board, current_player):
            clear_screen()
            show_instructions()
            draw_board(board)
            print(f"\nИгрок {player_name} выиграл!\n")
            scores[current_player] += 1
            break
        if check_draw(board):
            clear_screen()
            show_instructions()
            draw_board(board)
            print("\nНичья!\n")
            break
        current_player = switch_player(current_player)
    #print(f"Счёт: X - {scores['X']}, O - {scores['O']}")

    play_again = input("\nХотите сыграть ещё раз? (да/нет): ").strip().lower()
    if play_again != "да" and play_again != "yes":
        print("\nСпасибо за игру! До свидания!\n")
        break