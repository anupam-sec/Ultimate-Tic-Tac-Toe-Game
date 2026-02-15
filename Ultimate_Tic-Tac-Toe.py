import pygame
import math
import sys

# --- Configuration & Colors ---
WIDTH, HEIGHT = 850, 720 
BOARD_SIZE = 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
BLUE, RED = (40, 100, 250), (250, 50, 50)   
GRAY, DARK_GRAY = (220, 220, 220), (50, 50, 50)
GOLD, BUTTON_COLOR = (218, 165, 32), (100, 100, 100)
HIGHLIGHT = (200, 220, 255)
HINT_COLOR = (50, 180, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")
font_sm = pygame.font.SysFont("Arial", 18)
font_md = pygame.font.SysFont("Arial", 20, bold=True)
font_lg = pygame.font.SysFont("Arial", 28, bold=True)

class UltimateTicTacToe:
    def __init__(self):
        self.difficulty = "Medium"
        self.depth_map = {"Easy": 1, "Medium": 3, "Hard": 5}
        self.scores = {"Human": 0, "AI": 0, "Draws": 0}
        self.hint_move = None
        self.reset()

    def reset(self):
        self.board = [[' ' for _ in range(9)] for _ in range(9)]
        self.small_board_status = [' ' for _ in range(9)]
        self.next_board = -1 
        self.current_player = 'X' 
        self.winner = None
        self.history = []
        self.hint_move = None

    def check_line(self, cells):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for c in win_conditions:
            if cells[c[0]] == cells[c[1]] == cells[c[2]] != ' ' and cells[c[0]] != 'Draw':
                return cells[c[0]]
        # A board is a draw only if it's full AND no one won
        if ' ' not in cells:
            return 'Draw'
        return None

    def make_move(self, b_idx, c_idx, player):
        self.board[b_idx][c_idx] = player
        self.history.append(f"{player}: B{b_idx+1} C{c_idx+1}")
        self.hint_move = None # Clear hint after any move
        
        status = self.check_line(self.board[b_idx])
        if status:
            self.small_board_status[b_idx] = status
        
        self.winner = self.check_line(self.small_board_status)
        if self.winner:
            if self.winner == 'X': self.scores["Human"] += 1
            elif self.winner == 'O': self.scores["AI"] += 1
            else: self.scores["Draws"] += 1

        self.next_board = -1 if self.small_board_status[c_idx] != ' ' else c_idx

    def get_valid_moves(self):
        if self.winner: return []
        moves = []
        target = [self.next_board] if self.next_board != -1 else range(9)
        for b in target:
            if self.small_board_status[b] == ' ':
                for c in range(9):
                    if self.board[b][c] == ' ':
                        moves.append((b, c))
        return moves

    def minimax(self, depth, alpha, beta, is_max):
        res = self.check_line(self.small_board_status)
        if res == 'O': return 100 + depth
        if res == 'X': return -100 - depth
        if res == 'Draw': return 0
        if depth == 0: return 0
        
        moves = self.get_valid_moves()
        if not moves: return 0

        if is_max:
            best = -math.inf
            for b, c in moves:
                old = (self.board[b][c], self.small_board_status[b], self.next_board)
                self.board[b][c] = 'O'
                self.small_board_status[b] = self.check_line(self.board[b]) or ' '
                self.next_board = -1 if self.small_board_status[c] != ' ' else c
                best = max(best, self.minimax(depth-1, alpha, beta, False))
                self.board[b][c], self.small_board_status[b], self.next_board = old
                alpha = max(alpha, best)
                if beta <= alpha: break
            return best
        else:
            best = math.inf
            for b, c in moves:
                old = (self.board[b][c], self.small_board_status[b], self.next_board)
                self.board[b][c] = 'X'
                self.small_board_status[b] = self.check_line(self.board[b]) or ' '
                self.next_board = -1 if self.small_board_status[c] != ' ' else c
                best = min(best, self.minimax(depth-1, alpha, beta, True))
                self.board[b][c], self.small_board_status[b], self.next_board = old
                beta = min(beta, best)
                if beta <= alpha: break
            return best

    def get_hint(self):
        moves = self.get_valid_moves()
        if not moves: return
        best_val, best_move = math.inf, moves[0]
        for b, c in moves:
            old = (self.board[b][c], self.small_board_status[b], self.next_board)
            self.board[b][c] = 'X'
            self.small_board_status[b] = self.check_line(self.board[b]) or ' '
            self.next_board = -1 if self.small_board_status[c] != ' ' else c
            val = self.minimax(3, -math.inf, math.inf, True)
            self.board[b][c], self.small_board_status[b], self.next_board = old
            if val < best_val:
                best_val, best_move = val, (b, c)
        self.hint_move = best_move

    def draw_ui(self):
        pygame.draw.rect(screen, RED, (0, BOARD_SIZE, 600, 120))
        
        # Status
        status_txt = f"TURN: {'AI (O)' if self.current_player == 'O' else 'HUMAN (X)'}"
        if self.winner: 
            status_txt = "IT'S A DRAW!" if self.winner == 'Draw' else f"{'AI' if self.winner == 'O' else 'HUMAN'} WINS!"
        screen.blit(font_lg.render(status_txt, True, BLACK), (20, BOARD_SIZE + 10))
        
        score_txt = f"Human: {self.scores['Human']} | AI: {self.scores['AI']} | Draws: {self.scores['Draws']}"
        screen.blit(font_md.render(score_txt, True, DARK_GRAY), (20, BOARD_SIZE + 45))

        # Buttons
        self.reset_rect = pygame.Rect(480, BOARD_SIZE + 15, 100, 35)
        pygame.draw.rect(screen, BUTTON_COLOR, self.reset_rect, border_radius=5)
        screen.blit(font_md.render("RESET", True, WHITE), (505, BOARD_SIZE + 21))

        self.hint_rect = pygame.Rect(480, BOARD_SIZE + 60, 100, 35)
        pygame.draw.rect(screen, HINT_COLOR, self.hint_rect, border_radius=5)
        screen.blit(font_md.render("HINT", True, WHITE), (512, BOARD_SIZE + 66))

        # Difficulty
        screen.blit(font_md.render("Difficulty:", True, BLACK), (20, BOARD_SIZE + 85))
        self.diff_rects = {}
        for i, d in enumerate(["Easy", "Medium", "Hard"]):
            rect = pygame.Rect(120 + (i * 90), BOARD_SIZE + 80, 80, 30)
            pygame.draw.rect(screen, GOLD if self.difficulty == d else BUTTON_COLOR, rect, border_radius=5)
            screen.blit(font_md.render(d, True, WHITE), (rect.x + 10, rect.y + 3))
            self.diff_rects[d] = rect

        # Sidebar
        pygame.draw.rect(screen, DARK_GRAY, (600, 0, 250, HEIGHT))
        screen.blit(font_lg.render("MOVE HISTORY", True, WHITE), (640, 20))
        for i, move in enumerate(self.history[-25:]):
            color = BLUE if "X" in move else RED
            screen.blit(font_sm.render(move, True, color), (670, 60 + (i * 30)))

    def draw(self):
        screen.fill(WHITE)
        if self.next_board != -1 and not self.winner:
            r, c = divmod(self.next_board, 3)
            pygame.draw.rect(screen, HIGHLIGHT, (c*200, r*200, 200, 200))

        # Hint Highlight
        if self.hint_move:
            b, c = self.hint_move
            br, bc = divmod(b, 3)
            cr, cc = divmod(c, 3)
            pygame.draw.rect(screen, (200, 255, 200), (bc*200 + cc*66.6, br*200 + cr*66.6, 66.6, 66.6))

        for i in range(1, 9):
            w = 5 if i % 3 == 0 else 2
            pygame.draw.line(screen, BLACK, (i*66.6, 0), (i*66.6, BOARD_SIZE), w)
            pygame.draw.line(screen, BLACK, (0, i*66.6), (600, i*66.6), w)

        for b in range(9):
            br, bc = divmod(b, 3)
            if self.small_board_status[b] != ' ' and self.small_board_status[b] != 'Draw':
                color = BLUE if self.small_board_status[b] == 'X' else RED
                if self.small_board_status[b] == 'X':
                    pygame.draw.line(screen, color, (bc*200+40, br*200+40), (bc*200+160, br*200+160), 15)
                    pygame.draw.line(screen, color, (bc*200+160, br*200+40), (bc*200+40, br*200+160), 15)
                else:
                    pygame.draw.circle(screen, color, (bc*200+100, br*200+100), 70, 15)
            
            for c in range(9):
                cr, cc = divmod(c, 3)
                char = self.board[b][c]
                if char != ' ':
                    color = BLUE if char == 'X' else RED
                    pos = (bc*200 + cc*66 + 33, br*200 + cr*66 + 33)
                    screen.blit(font_md.render(char, True, color), (pos[0]-10, pos[1]-10))
        self.draw_ui()

def main():
    game = UltimateTicTacToe()
    while True:
        game.draw()
        pygame.display.flip()
        if game.current_player == 'O' and not game.winner:
            pygame.time.wait(300) 
            moves = game.get_valid_moves()
            if moves:
                best_val, move = -math.inf, moves[0]
                for b_idx, c_idx in moves:
                    old = (game.board[b_idx][c_idx], game.small_board_status[b_idx], game.next_board)
                    game.board[b_idx][c_idx] = 'O'
                    game.small_board_status[b_idx] = game.check_line(game.board[b_idx]) or ' '
                    game.next_board = -1 if game.small_board_status[c_idx] != ' ' else c_idx
                    val = game.minimax(game.depth_map[game.difficulty], -math.inf, math.inf, False)
                    game.board[b_idx][c_idx], game.small_board_status[b_idx], game.next_board = old
                    if val > best_val: best_val, move = val, (b_idx, c_idx)
                game.make_move(move[0], move[1], 'O')
                game.current_player = 'X'

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if game.reset_rect.collidepoint(mx, my): game.reset()
                if game.hint_rect.collidepoint(mx, my) and not game.winner: game.get_hint()
                for d, rect in game.diff_rects.items():
                    if rect.collidepoint(mx, my): game.difficulty = d
                if game.current_player == 'X' and not game.winner and mx < 600 and my < BOARD_SIZE:
                    b_idx = (my // 200) * 3 + (mx // 200)
                    c_idx = ((my % 200) // 66) * 3 + ((mx % 200) // 66)
                    if (b_idx, c_idx) in game.get_valid_moves():
                        game.make_move(b_idx, c_idx, 'X')
                        if not game.winner: game.current_player = 'O'

if __name__ == "__main__":
    main()