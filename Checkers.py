import tkinter as tk
from tkinter import messagebox
import random
import hashlib
import os

# Константы
PLAYER1_NAME = "Белый"
PLAYER2_NAME = "Черный"
PLAYERS_FILE = "players.txt"
USERS_FILE = "users.txt"

BOARD_SIZE = 8
EMPTY = 0
WHITE = 1
BLACK = 2
WHITE_KING = 3
BLACK_KING = 4

LIGHT_SQUARE = "white"
DARK_SQUARE = "#808080"  # Серый
TEXT_COLOR = "black"
WHITE_PIECE = "white"
BLACK_PIECE = "red"
KING_CROWN = "gold"
SELECTED_OUTLINE = "gold"

# Шрифт Cormorant Infant с fallback
try:
    from tkinter.font import Font
    FONT_NAME = "Cormorant Infant"
    font_test = Font(family=FONT_NAME, size=12)
except:
    FONT_NAME = "Arial"


# Функции хеширования и работы с пользователями
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def hash_name(name):
    return hashlib.sha256(name.encode('utf-8')).hexdigest()[:8]


def save_user(username, password):
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{hash_password(password)}\n")


def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
    return users


# Окна авторизации и регистрации
def show_login_window(player_num):
    def login_user():
        username = entry_username.get().strip()
        password = entry_password.get()
        users_db = load_users()
        hashed_pw = hash_password(password)

        if users_db.get(username) == hashed_pw:
            global PLAYER1_NAME, PLAYER2_NAME
            if player_num == 1:
                PLAYER1_NAME = username
                login_root.destroy()
                show_register_window(2)
            else:
                PLAYER2_NAME = username
                login_root.destroy()
                show_names_window()
        else:
            messagebox.showerror("Ошибка", f"Неверный логин или пароль для Игрока {player_num}.")

    login_root = tk.Tk()
    login_root.title(f"Вход Игрока {player_num}")
    login_root.geometry("300x200")

    tk.Label(login_root, text=f"Игрок {player_num} (Логин):").pack(pady=5)
    entry_username = tk.Entry(login_root)
    entry_username.pack()

    tk.Label(login_root, text="Пароль:").pack(pady=5)
    entry_password = tk.Entry(login_root, show="*")
    entry_password.pack()

    tk.Button(login_root, text="Войти", command=login_user).pack(pady=10)
    tk.Button(login_root, text="Зарегистрироваться", command=lambda: [login_root.destroy(), show_register_window(player_num)]).pack(pady=5)

    login_root.mainloop()


def show_register_window(player_num):
    def register_user():
        username = entry_username.get().strip()
        password = entry_password.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль должны быть заполнены.")
            return

        users_db = load_users()
        if username in users_db:
            messagebox.showerror("Ошибка", f"Пользователь с логином '{username}' уже существует.")
            return

        save_user(username, password)
        messagebox.showinfo("Успех", f"Регистрация Игрока {player_num} завершена. Войдите в аккаунт.")
        register_root.destroy()
        show_login_window(player_num)

    register_root = tk.Tk()
    register_root.title(f"Регистрация Игрока {player_num}")
    register_root.geometry("300x200")

    tk.Label(register_root, text=f"Логин Игрока {player_num}:").pack(pady=5)
    entry_username = tk.Entry(register_root)
    entry_username.pack()

    tk.Label(register_root, text="Пароль:").pack(pady=5)
    entry_password = tk.Entry(register_root, show="*")
    entry_password.pack()

    tk.Button(register_root, text="Зарегистрироваться", command=register_user).pack(pady=10)
    tk.Button(register_root, text="Назад", command=lambda: [
        register_root.destroy(),
        show_start_window() if player_num == 1 else show_login_window(1)
    ]).pack(pady=5)

    register_root.mainloop()


def show_names_window():
    def start_game():
        global PLAYER1_NAME, PLAYER2_NAME
        name1 = entry1.get().strip()
        name2 = entry2.get().strip()
        if name1 and name2:
            PLAYER1_NAME = name1
            PLAYER2_NAME = name2
            with open(PLAYERS_FILE, "a", encoding="utf-8") as f:
                hashed1 = hash_name(PLAYER1_NAME)
                hashed2 = hash_name(PLAYER2_NAME)
                f.write(f"{hashed1} vs {hashed2}\n")
            names_root.destroy()
            GameGUI()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите оба имени.")

    names_root = tk.Tk()
    names_root.title("Введите имена игроков")
    names_root.geometry("300x150")

    tk.Label(names_root, text=f"Игрок 1 ({PLAYER1_NAME}):").pack(pady=5)
    entry1 = tk.Entry(names_root)
    entry1.pack()
    entry1.insert(0, PLAYER1_NAME)

    tk.Label(names_root, text=f"Игрок 2 ({PLAYER2_NAME}):").pack(pady=5)
    entry2 = tk.Entry(names_root)
    entry2.pack()
    entry2.insert(0, PLAYER2_NAME)

    tk.Button(names_root, text="Начать игру", command=start_game).pack(pady=10)
    names_root.mainloop()


def show_start_window():
    def start_registration():
        start_root.destroy()
        show_register_window(1)

    def start_login():
        start_root.destroy()
        show_login_window(1)

    start_root = tk.Tk()
    start_root.title("Царские башни — Поддавки")
    start_root.geometry("300x150")
    tk.Label(start_root, text="Добро пожаловать в игру!", font=(FONT_NAME, 14)).pack(pady=10)
    tk.Button(start_root, text="Зарегистрироваться", command=start_registration).pack(pady=5)
    tk.Button(start_root, text="Войти", command=start_login).pack(pady=5)
    start_root.mainloop()


# Логика игры
class GameEngine:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = random.choice([WHITE, BLACK])
        self.move_count = 0

    def create_initial_board(self):
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # Белые (нижние 3 ряда)
        for r in range(5, 8):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 == 1:
                    board[r][c] = WHITE
        board[7][0] = WHITE_KING  # дамка на H1

        # Чёрные (верхние 3 ряда)
        for r in range(3):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 == 1:
                    board[r][c] = BLACK
        board[0][1] = BLACK_KING  # дамка на B8
        return board

    def is_player_piece(self, piece, player):
        if player == WHITE:
            return piece in (WHITE, WHITE_KING)
        return piece in (BLACK, BLACK_KING)

    def get_all_moves(self, player):
        moves = []
        captures = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if not self.is_player_piece(piece, player):
                    continue
                piece_moves, piece_caps = self.get_piece_moves(r, c, player)
                moves.extend(piece_moves)
                captures.extend(piece_caps)

        if captures:
            max_len = max(len(cap[4]) for cap in captures)
            captures = [cap for cap in captures if len(cap[4]) == max_len]
            return [], captures
        return moves, []

    def get_piece_moves(self, r, c, player):
        piece = self.board[r][c]
        is_king = piece in (WHITE_KING, BLACK_KING)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves = []
        captures = []

        if not is_king:
            dr = -1 if piece == WHITE else 1
            for dc in [-1, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if self.board[nr][nc] == EMPTY:
                        moves.append((r, c, nr, nc))

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                br, bc = r + 2 * dr, c + 2 * dc
                if (0 <= br < BOARD_SIZE and 0 <= bc < BOARD_SIZE and
                    0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                    if (self.board[nr][nc] != EMPTY and
                        not self.is_player_piece(self.board[nr][nc], player)):
                        if self.board[br][bc] == EMPTY:
                            captures.append((r, c, br, bc, [(nr, nc)]))
        else:
            # Дамка — простые ходы
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if self.board[nr][nc] == EMPTY:
                        moves.append((r, c, nr, nc))
                    else:
                        break
                    nr += dr
                    nc += dc
            # Дамка — взятия
            for dr, dc in directions:
                self._explore_king_capture(r, c, dr, dc, [], captures, player)

        return moves, captures

    def _explore_king_capture(self, r, c, dr, dc, captured_list, all_captures, player):
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            if self.board[nr][nc] != EMPTY and not self.is_player_piece(self.board[nr][nc], player):
                nnr, nnc = nr + dr, nc + dc
                while 0 <= nnr < BOARD_SIZE and 0 <= nnc < BOARD_SIZE:
                    if self.board[nnr][nnc] == EMPTY:
                        new_captured = captured_list + [(nr, nc)]
                        all_captures.append((r, c, nnr, nnc, new_captured))
                        self._explore_king_capture(nnr, nnc, dr, dc, new_captured, all_captures, player)
                    else:
                        break
                    nnr += dr
                    nnc += dc
                break
            elif self.board[nr][nc] != EMPTY:
                break
            nr += dr
            nc += dc

    def make_move(self, move, is_capture=False):
        r1, c1, r2, c2 = move[:4]
        piece = self.board[r1][c1]
        self.board[r1][c1] = EMPTY
        self.board[r2][c2] = piece

        if is_capture:
            for (cr, cc) in move[4]:
                self.board[cr][cc] = EMPTY

        # Превращение в дамку
        if piece == WHITE and r2 == 0:
            self.board[r2][c2] = WHITE_KING
        if piece == BLACK and r2 == 7:
            self.board[r2][c2] = BLACK_KING

        self.move_count += 1

    def check_end(self):
        moves, captures = self.get_all_moves(self.current_player)
        has_pieces = any(
            self.is_player_piece(self.board[r][c], self.current_player)
            for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
        )
        if not has_pieces or (not moves and not captures):
            return True
        return False

    def switch_player(self):
        self.current_player = WHITE if self.current_player == BLACK else BLACK

    def evaluate_position(self):
        count = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if self.is_player_piece(piece, self.current_player):
                    count += 1
        return count


# Графический интерфейс
class GameGUI:
    CELL_SIZE = 60

    def __init__(self):
        self.engine = GameEngine()
        self.root = tk.Tk()
        self.root.title("Царские башни — Поддавки")

        canvas_width = 8 * self.CELL_SIZE + 80
        canvas_height = 8 * self.CELL_SIZE + 80
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.selected = None
        self.highlight_moves = []
        self.message = tk.Label(self.root, text="", font=(FONT_NAME, 12), fg=TEXT_COLOR)
        self.message.pack()

        self.draw_board()
        self.update_turn_label()
        self.root.mainloop()

    def draw_board(self):
        self.canvas.delete("all")
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        offset_x = 40
        offset_y = 40

        # Координаты
        for i, letter in enumerate(letters):
            x = offset_x + (i + 0.5) * self.CELL_SIZE
            y = offset_y - 15
            self.canvas.create_text(x, y, text=letter, font=(FONT_NAME, 12, "bold"), fill=TEXT_COLOR)

        for i, number in enumerate(numbers):
            x = offset_x - 15
            y = offset_y + (7 - i + 0.5) * self.CELL_SIZE
            self.canvas.create_text(x, y, text=number, font=(FONT_NAME, 12, "bold"), fill=TEXT_COLOR)

        for i, number in enumerate(numbers):
            x = offset_x + 8 * self.CELL_SIZE + 15
            y = offset_y + (7 - i + 0.5) * self.CELL_SIZE
            self.canvas.create_text(x, y, text=number, font=(FONT_NAME, 12, "bold"), fill=TEXT_COLOR)

        for i, letter in enumerate(letters):
            x = offset_x + (i + 0.5) * self.CELL_SIZE
            y = offset_y + 8 * self.CELL_SIZE + 15
            self.canvas.create_text(x, y, text=letter, font=(FONT_NAME, 12, "bold"), fill=TEXT_COLOR)

        # Доска
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = offset_x + c * self.CELL_SIZE
                y1 = offset_y + (7 - r) * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                color = DARK_SQUARE if (r + c) % 2 == 1 else LIGHT_SQUARE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=TEXT_COLOR, width=1)

        # Подсветка возможных ходов
        for (rr, cc) in self.highlight_moves:
            x1 = offset_x + cc * self.CELL_SIZE
            y1 = offset_y + (7 - rr) * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)

        # Шашки
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.engine.board[r][c]
                if piece != EMPTY:
                    self.draw_piece(r, c, piece, offset_x, offset_y)

    def draw_piece(self, r, c, piece, offset_x, offset_y):
        x = offset_x + c * self.CELL_SIZE + self.CELL_SIZE // 2
        y = offset_y + (7 - r) * self.CELL_SIZE + self.CELL_SIZE // 2
        color = WHITE_PIECE if piece in (WHITE, WHITE_KING) else BLACK_PIECE
        outline = KING_CROWN if piece in (WHITE_KING, BLACK_KING) else TEXT_COLOR

        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline=outline, width=2)

        if self.selected and self.selected == (r, c):
            self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline=SELECTED_OUTLINE, width=4)

    def on_click(self, event):
        offset_x, offset_y = 40, 40
        x = event.x - offset_x
        y = event.y - offset_y

        if x < 0 or y < 0 or x >= 8 * self.CELL_SIZE or y >= 8 * self.CELL_SIZE:
            return

        c = int(x // self.CELL_SIZE)
        r = 7 - int(y // self.CELL_SIZE)

        if not self.selected:
            piece = self.engine.board[r][c]
            if self.engine.is_player_piece(piece, self.engine.current_player):
                self.selected = (r, c)
                self.show_possible_moves(r, c)
        else:
            r1, c1 = self.selected
            self.try_move(r1, c1, r, c)
            self.selected = None
            self.highlight_moves = []
            self.draw_board()
            if self.engine.check_end():
                self.show_winner()

    def show_possible_moves(self, r, c):
        moves, captures = self.engine.get_all_moves(self.engine.current_player)
        if not moves and not captures:
            if self.engine.check_end():
                self.show_winner()
            return

        self.highlight_moves = []
        if captures:
            for cap in captures:
                if cap[0] == r and cap[1] == c:
                    self.highlight_moves.append((cap[2], cap[3]))
        else:
            for mv in moves:
                if mv[0] == r and mv[1] == c:
                    self.highlight_moves.append((mv[2], mv[3]))

    def try_move(self, r1, c1, r2, c2):
        moves, captures = self.engine.get_all_moves(self.engine.current_player)
        move_normal = (r1, c1, r2, c2)

        for cap in captures:
            if cap[0] == r1 and cap[1] == c1 and cap[2] == r2 and cap[3] == c2:
                self.engine.make_move(cap, is_capture=True)
                new_moves, new_caps = self.engine.get_piece_moves(r2, c2, self.engine.current_player)
                continuing_caps = [cap for cap in new_caps if cap[0] == r2 and cap[1] == c2]
                if continuing_caps:
                    self.selected = (r2, c2)
                    self.show_possible_moves(r2, c2)
                    return
                self.engine.switch_player()
                self.update_turn_label()
                return

        if captures:
            self.message.config(text="Бой обязательный!")
            return

        for mv in moves:
            if mv == move_normal:
                self.engine.make_move(mv)
                self.engine.switch_player()
                self.update_turn_label()
                return

        self.message.config(text="Неверный ход")

    def update_turn_label(self):
        color = "Белые" if self.engine.current_player == WHITE else "Черные"
        name = PLAYER1_NAME if self.engine.current_player == WHITE else PLAYER2_NAME
        moves = self.engine.move_count
        self.message.config(text=f"Ход: {name} ({color}) | Ходов: {moves}")
        if self.engine.check_end():
            self.show_winner()

    def show_winner(self):
        loser = "Белые" if self.engine.current_player == WHITE else "Черные"
        winner = "Черные" if loser == "Белые" else "Белые"
        name_winner = PLAYER2_NAME if loser == "Белые" else PLAYER1_NAME

        self.root.withdraw()
        self.ask_rematch(winner, name_winner)

    def ask_rematch(self, winner_color, winner_name):
        self.rematch_window = tk.Toplevel()
        self.rematch_window.title("Игра окончена")
        self.rematch_window.geometry("250x100")
        self.rematch_window.resizable(False, False)

        tk.Label(self.rematch_window, text=f"Победа: {winner_name} ({winner_color})", font=(FONT_NAME, 12)).pack(pady=10)

        button_frame = tk.Frame(self.rematch_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Новая игра", command=self.start_new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Выход", command=self.exit_game).pack(side=tk.LEFT, padx=5)

    def start_new_game(self):
        self.rematch_window.destroy()
        self.root.destroy()
        show_start_window()

    def exit_game(self):
        self.rematch_window.destroy()
        self.root.quit()


if __name__ == "__main__":
    show_start_window()