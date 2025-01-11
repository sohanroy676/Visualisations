import pygame

class NQueens_BitManip:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.reset()
    
    def reset(self) -> None:
        self.bitboard: int = 0
        self.history: list[int] = []        
        self.queens: list[int] = []
        self.queens_len: int = len(self.queens)
        self.start: int = 0

    def place(self, row: int, col: int) -> None:
        if self.bitboard & (1 << (row * self.n + col)): return
        self.queens.append(col)
        self.history.append(self.bitboard)
        self.queens_len += 1
        #Horizontal
        mask: int = int('1'*self.n, 2) << (row * self.n)
        #Vertical
        mask |= int(('0'*(self.n - 1) + '1')*self.n, 2) << col
        #Major Diagonal
        for i in range(self.n):
            diag = 1 << i
            if row < col:
                diag <<= col - row
            elif row > col:
                diag >>= row - col
            diag &= int('1'*self.n, 2)
            mask |= diag << i*self.n
        #Minor Diagonal
        for i in range(self.n):
            diag = 1 << (self.n - i - 1)
            if row + col + 1 < self.n:
                diag >>= self.n - row - col - 1
            elif row + col + 1 > self.n:
                diag <<= row + col - self.n + 1
            diag &= int('1'*self.n, 2)
            mask |= diag << i*self.n
        self.bitboard |= mask
    
    def get_possible(self, row: int, start: int = 0) -> list[int]:
        return [i for i in range(start, self.n) if not (self.bitboard & (1 << (row*self.n + i)))]

    def get_not_possible(self, row: int) -> list[int]:
        return [i for i in range(self.n) if (self.bitboard & (1 << (row*self.n + i)))]
    
    def next(self) -> None:
        possible: list[int] = self.get_possible(self.queens_len, self.start)
        if (not possible):
            self.bitboard = self.history.pop()
            self.start = self.queens.pop() + 1
            self.queens_len -= 1
            return
        self.place(self.queens_len, possible[0])
        self.start = 0
    
    def update(self) -> None:
        if self.queens_len < self.n:
            self.next()
            if self.queens_len == self.n:
                print("Solution: " + str(self.queens))
                return True
        return False

class NQueens:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.reset()
    
    def reset(self) -> None:
        self.board: list[list[int]] = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.history: list[list[list[int]]] = []
        self.queens: list[int] = []
        self.queens_len: int = len(self.queens)
        self.start: int = 0
    
    def update(self) -> bool:
        if self.queens_len < self.n:
            self.next()
            if self.queens_len == self.n:
                print("Solution: " + str(self.queens))
                return True
        return False
    
    def place(self, row: int, col: int) -> None:
        if self.board[row][col]: return
        self.queens.append(col)
        self.history.append([i[:] for i in self.board])
        self.queens_len += 1
        
        for i in range(self.n):
            self.board[row][i] = 1 # Horizontal
            self.board[i][col] = 1 # Vertical
        
        # Major Diagonal
        diag: int = min(row, col)
        diag_row: int = row - diag
        diag_col: int = col - diag
        for i in range(self.n):
            if diag_row >= self.n or diag_col >= self.n: break
            self.board[diag_row][diag_col] = 1
            diag_row += 1
            diag_col += 1
        
        # Minor diagonal
        diag = min(row, self.n - col - 1)
        diag_row = row - diag
        diag_col = col + diag
        for i in range(self.n):
            if diag_row >= self.n or diag_col < 0: break
            self.board[diag_row][diag_col] = 1
            diag_row += 1
            diag_col -= 1
    
    def get_possible(self, row: int, start: int = 0) -> list[int]:
        return [i for i in range(start, self.n) if not self.board[row][i]]

    def get_not_possible(self, row: int) -> list[int]:
        return [i for i in range(self.n) if self.board[row][i]]

    def next(self) -> None:
        possible: list[int] = self.get_possible(self.queens_len, self.start)
        if (not possible):
            self.board = self.history.pop()
            self.start = self.queens.pop() + 1
            self.queens_len -= 1
            return
        self.place(self.queens_len, possible[0])
        self.start = 0

class App:
    def __init__(self) -> None:
        print("Running the N-Queens Visualisation")
        self.n: int = int(input("Enter N: "))
        self.cell_size = 50
        
        # self.vis: NQueens | NQueens_BitManip = NQueens_BitManip(self.n)
        self.vis: NQueens | NQueens_BitManip = NQueens(self.n)

        self.win_width: int = self.n*self.cell_size
        self.win_height: int = self.n*self.cell_size
        self.WIN: pygame.Surface = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("N-Queens Visualisation")

        self.img: pygame.Surface = pygame.image.load("W_Queen.png")
        self.img.set_colorkey((181, 230, 29))
        self.img = pygame.transform.scale(self.img, (self.cell_size, self.cell_size))

        self.surf: pygame.Surface = pygame.Surface((self.cell_size*self.n, self.cell_size*self.n))
        self.rect: pygame.Rect = self.surf.get_rect()
        self.rect.center = (self.win_width//2, self.win_height//2)

        self.board: pygame.Surface = pygame.Surface((self.cell_size*self.n, self.cell_size*self.n))
        self.board.fill((235, 236, 208))

        [pygame.draw.rect(self.board, (119, 149, 86), (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size))
                            for r in range(self.n) for c in range(self.n) if (r + c)%2]

        self.timer: int = 0
        self.time: int = 500

        self.test_time()
    
    def draw_queens(self) -> None:
        [self.surf.blit(self.img, (col*self.cell_size, row*self.cell_size)) for row, col in enumerate(self.vis.queens)]
    
    def draw_queen_moves(self) -> None:
        [pygame.draw.rect(self.surf, (255, 0, 0), (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size))
            for r in range(self.n) for c in self.vis.get_not_possible(r)]

    def draw(self) -> None:
        self.surf.blit(self.board, (0, 0))
        self.draw_queen_moves()
        self.draw_queens()
        self.WIN.blit(self.surf, self.rect)
        pygame.display.update()
    
    def test_time(self) -> None:
        from time import time
        vis_bitm: NQueens_BitManip = NQueens_BitManip(self.n)
        start: int = time()
        while not vis_bitm.update():
            pass
        end: int = time()
        print(f"BitManipulation took {end - start}")

        vis_norm: NQueens = NQueens(self.n)
        start = time()
        while not vis_norm.update():
            pass
        end = time()
        print(f"Normal took: {end - start}")

    def mainloop(self) -> None:
        run: bool = True
        while run:
            if pygame.event.get(pygame.QUIT):
                run = False

            self.timer += 1
            if self.timer >= self.time:
                self.vis.update()
                self.timer %= self.time
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    app: App = App()
    app.mainloop()