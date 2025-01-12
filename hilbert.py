import pygame
from utils import HSVToRGB, Vec2, remap

class App:
    ORDER: int = 8
    N: int = pow(2, ORDER)
    POINTS: int = N*N
    SURFDIM: int = pow(2, ORDER+1)
    LEN: int = SURFDIM / N

    def __init__(self, WIN) -> None:
        print("Starting the visualisation for an N-order Hilbert Curve")
        print("S to save the image of the generated curve into 'assets' folder")

        self.WIN: pygame.Surface = WIN
        self.SURF: pygame.Surface = pygame.Surface((App.SURFDIM, App.SURFDIM))
        pygame.display.set_caption("Hilbert Curve")
        self.SURF.fill((0, 0, 0))

        WINRect: pygame.Rect = self.WIN.get_rect()
        self.blitPos: tuple[int] = ((WINRect.width - App.SURFDIM)//2, (WINRect.height - App.SURFDIM)//2)

        self.fps: int = 60
        self.index: int = 1
        self.getPath()
        self.clock = pygame.time.Clock()

    def hilbert(self, i: int) -> Vec2:
        points: list[Vec2] = [Vec2(0, 0), Vec2(0, 1), Vec2(1, 1), Vec2(1, 0)]
        idx: int = i & 3
        vec: Vec2 = points[idx]
        for j in range(1, App.ORDER):
            length = pow(2, j)
            i >>= 2
            idx = i & 3
            if idx == 0: 
                vec.x, vec.y = vec.y, vec.x
            elif idx == 1:
                vec.y += length
            elif idx == 2:
                vec.y += length
                vec.x += length
            elif idx == 3:
                vec.x, vec.y = length-1-vec.y, length-1-vec.x
                vec.x += length
        return vec

    def getPath(self) -> None:
        self.path: list[Vec2] = []
        for i in range(App.POINTS):
            self.path.append(self.hilbert(i))
            self.path[i] *= App.LEN
            self.path[i] += Vec2(App.LEN/2, App.LEN/2)

    def getColor(self) -> tuple[int]:
        return HSVToRGB(remap(0, App.POINTS, 0, 360, self.index), 1, 1)

    def mainloop(self) -> bool:
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        return False
                    
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.quit()
                                return True
                            case pygame.K_s:
                                pygame.image.save(self.SURF, f"assets\\hilbert{App.ORDER}.png")
                    
                    case pygame.MOUSEBUTTONDOWN:
                        match event.button:
                            case 4: self.fps += 10
                            case 5: self.fps = max(self.fps-10, 0)
            
            if self.index < App.POINTS:
                pygame.draw.line(self.SURF, self.getColor(), list(self.path[self.index-1]), list(self.path[self.index]))
                pygame.display.update(self.WIN.blit(self.SURF, self.blitPos))
                self.index += 1

    def quit(self) -> None:
        pygame.display.set_caption("Visualisations")

if __name__ == "__main__":
    WIN: pygame.Surface = pygame.display.set_mode((App.SURFDIM, App.SURFDIM))
    app: App = App(WIN)
    app.mainloop()
    pygame.quit()