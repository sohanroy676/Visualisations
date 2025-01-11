'''
A* Path Finding Algorithm for 2D Grid without diagonal movement
'''
import pygame
from utils import drawGridLines

class Node:
    def __init__(self, row: int, col: int, parent, goal: list[int]) -> None:
        self.row: int = row
        self.col: int = col
        self.parent: Node = parent
        self.g: int = 0 if self.parent is None else self.parent.g + 1
        self.h: int = self.getDist(goal)
        self.f: int = self.g + self.h
    
    def update(self, parent) -> None:
        newG: int = parent.g + 1
        if newG >= self.g: return
        self.parent = parent
        self.g: int = newG
        self.f: int = self.h + self.g

    def getDist(self, pt: list[int]) -> int:
        return abs(self.row - pt[0]) + abs(self.col - pt[1])
    
    def getDistFromNode(self, other) -> int:
        return self.getDist([other.row, other.col])

    def isSame(self, other) -> bool:
        if isinstance(other, Node): return (self.row == other.row and self.col == other.col)
        return (self.row == other[0] and self.col == other[1])

    def __repr__(self) -> str:
        return f"({self.row}, {self.col}) : ({self.g}, {self.h}, {self.f})"

class Astar:
    states: dict[str: int] = {"wall": 0, "empty": 1, "start": 2, "goal": 3}
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.solveStarted: bool = False
        self.current: Node = None
        self.open: list = []
        self.closed: list = []
        self.path: list = []
        self.resetGrid()
        App.instance.resetSurf()

    def resetGrid(self) -> None:
        self.grid: list[list[int]] = [[1 for j in range(App.COLS)] for i in range(App.ROWS)]
        self.endPoints: list[list[int]] = [[-1, -1], [-1, -1]]
    
    def place(self, pos: tuple[int], state: int) -> None:
        if pos[0] < 0 or pos[0] >= App.ROWS or pos[1] < 0 or pos[1] >= App.COLS: return
        self.grid[pos[0]][pos[1]] = state
        if state in [self.states["start"], self.states["goal"]]: self.endPoints[state-2] = pos[:]
        App.instance.updateGrid(*pos, App.COLORSLIST[state])
    
    def getNeighbors(self) -> list[list[int]]:
        n: list[list[int]] = []
        r: int = self.current.row
        c: int = self.current.col
        for i in [[r-1, c], [r+1, c], [r, c-1], [r, c+1]]:
            if 0 <= i[0] < App.ROWS and 0 <= i[1] < App.COLS and self.grid[i[0]][i[1]]:
                n.append(i)
        return n[:]

    def solveStart(self) -> None:
        self.open.append(Node(*self.endPoints[0], None, self.endPoints[1]))
        self.solveStarted: bool = True

    def solveNext(self) -> None:
        self.current: Node = self.getFromOpen()
        self.closed.append(self.current)
        if (not self.current.isSame(self.endPoints[0])) and (not self.current.isSame(self.endPoints[1])):
            App.instance.updateGrid(self.current.row, self.current.col, App.COLORS["closed"])

        if self.current.isSame(self.endPoints[1]):
            self.getPath()
            self.solveStarted = False
            return
        
        for n in self.getNeighbors():
            if self.inLst(self.closed, n) >= 0: continue
            
            openIdx = self.inLst(self.open, n)
            if openIdx < 0:
                self.open.append(Node(n[0], n[1], self.current, self.endPoints[1]))
                App.instance.updateGrid(*n, App.COLORS["open"])
            self.open[openIdx].update(self.current)

    def getPath(self) -> None:
        self.path: list[Node] = [self.current]
        parent: Node = self.current.parent
        while parent is not None:
            self.path.append(parent)
            parent = parent.parent
        for i in App.instance.astar.path:
            App.instance.updateGrid(i.row, i.col, App.COLORS["goal"])
        drawGridLines(App.instance.surf, App.ROWS, App.COLS, App.SIDE, App.COLORS["wall"], True)

    def inLst(self, lst, node) -> int:
        for i, n in enumerate(lst):
            if n.isSame(node): return i
        return -1

    def getFromOpen(self) -> Node:
        idx: int = 0
        for i, n in enumerate(self.open):
            if i == idx or n.f < self.open[idx].f: idx = i
        return self.open.pop(idx)

class App:
    SIDE: int = 10
    WIDTH: int = 1000
    HEIGHT: int = 700
    ROWS: int = HEIGHT//SIDE
    COLS: int = WIDTH//SIDE
    FPS: int = 60
    COLORS: dict[str: tuple[int]] = {"wall": (0, 0, 0), "empty": (255, 255, 255), "start": (0, 0, 255), "goal": (100, 200, 255), "open": (0, 255, 0), "closed": (255, 0, 0)}
    COLORSLIST: list[tuple[int]] = [i for i in COLORS.values()]
    blitPos: tuple[int] = (0, 0)
    instance = None

    def __init__(self, WIN: pygame.Surface) -> None:
        print("Starting the Visualisation for A* Pathfinding Algorithm")
        print("ESC to Quit")
        print("Enter to start solving")
        print("BACKSPACE | R to Clear")
        print("LEFT_CLICK to place Wall")
        print("RIGHT_CLICK to remove Wall")
        print("SCROLL_WHEEL_UP to place the Start Point")
        print("SCROLL_WHEEL_DOWN to place the End Point")
        
        App.instance = self

        self.WIN: pygame.Surface = WIN
        self.WINRect: pygame.Rect = WIN.get_rect()

        App.blitPos: tuple[int] = ((self.WINRect.width - App.WIDTH)//2, (self.WINRect.height - App.HEIGHT)//2)

        self.surf: pygame.Surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.surfRect: pygame.Rect = self.surf.get_rect()
        pygame.display.set_caption("A* Pathfinder")

        self.astar: Astar = Astar()
        self.mouseState: dict = {"down": False, "state": 0}
        self.clock = pygame.time.Clock()

    def update(self) -> None:
        pygame.display.update(self.WIN.blit(self.surf, App.blitPos))
    
    def updateGrid(self, row, col, clr) -> None:
        pygame.draw.rect(self.surf, clr, (col*App.SIDE, row*App.SIDE, App.SIDE, App.SIDE))
        self.update()
    
    def resetSurf(self) -> None:
        self.surf.fill(App.COLORS["empty"])
        drawGridLines(self.surf, App.ROWS, App.COLS, App.SIDE, App.COLORS["wall"])
        self.update()
    
    def getPosFromMouse() -> tuple[int]:
        pos = pygame.mouse.get_pos()
        return ((pos[1] - App.blitPos[1])//App.SIDE, (pos[0] - App.blitPos[0])//App.SIDE)

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(App.FPS)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_RETURN:
                                self.astar.solveStart()
                            case pygame.K_BACKSPACE | pygame.K_r:
                                self.astar.reset()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case 1 | 3:
                                self.mouseState["down"] = True
                                self.mouseState["state"] = 0 if event.button == 1 else 1
                            case 4 | 5:
                                # 4 = SCROLL_WHEEL_UP, 5 = SCROLL_WHEEL_DOWN
                                if not self.astar.solveStarted:
                                    self.astar.place(App.getPosFromMouse(), Astar.states[["start", "goal"][event.button-4]])
                    
                    case pygame.MOUSEBUTTONUP:
                        self.mouseState["down"] = False
                        if self.astar.solveStarted: App.FPS += 20

            if self.astar.solveStarted: self.astar.solveNext()
            elif self.mouseState["down"]: self.astar.place(App.getPosFromMouse(), self.mouseState["state"])
        
    
    def quit(self):
        pygame.display.set_caption("Visualizations")

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
    app: App = App(WIN)
    app.mainloop()