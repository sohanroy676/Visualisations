'''
The main menu to select the visualisation
'''
import pygame
from utils import Label, Button
pygame.init()

class MainApp:
    WIDTH: int = 1280
    HEIGHT: int = 720
    COLORS: dict = {"bg": pygame.Color("purple")}
    APPS: list[str] = ["Astar", "Hilbert", "Life", "MarchSq", "Sand", "NQueens", "Sort"]

    def __init__(self) -> None:
        '''Initializing the main app'''
        self.WIN: pygame.Surface = pygame.display.set_mode((MainApp.WIDTH, MainApp.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Visualisations")
        
        self.run: bool = True
        self.app = None

        self.loadUIElements()
    
    def clearScreen(self, update: bool = False) -> None:
        '''Clears the window by filling it the background color'''
        self.WIN.fill(self.COLORS["bg"])
        if update:
            pygame.display.update()

    def draw(self) -> None:
        self.clearScreen()
        self.drawUIElements()
        pygame.display.update()
    
    def loadUIElements(self) -> None:
        '''Loads the UI elements like Labels and Buttons'''
        # Sets the default values of the UI elements for this project.
        Label.setDefault(foreground=(255, 0, 0), background=(50, 50, 50), borderRadius = 10)

        # Adding the Labels
        self.labels: list[Label] = []
        self.labels.append(Label("Visualizations", (MainApp.WIDTH//2, MainApp.WIDTH//10), size = 80))

        # Adding the Buttons
        self.buttons: list[Button] = []
        self.buttons.append(Button("Quit", (MainApp.WIDTH//2, 9*MainApp.HEIGHT//10), self.quit, size = 30))
        cols: int = 4
        for i, name in enumerate(MainApp.APPS):
            button: Button = Button(name, (2*(i%cols + 1)*MainApp.WIDTH//10, 2*(2 + i//cols)*MainApp.HEIGHT//10), 
                                    lambda: self.setApp(name.lower()))
            self.buttons.append(button)
        
        self.buttons: list[Button] = [
                Button(name, (2*(i%cols + 1)*MainApp.WIDTH//10, 2*(2 + i//cols)*MainApp.HEIGHT//10), 
                                lambda: self.setApp(name.lower()))
                for i, name in enumerate(MainApp.APPS)
            ]

    
    def drawUIElements(self) -> None:
        '''Draws the UI elements like Labels and Buttons'''
        # Drawing the labels
        for label in self.labels:
            label.draw(self.WIN)
        
        # Drawing the buttons
        for button in self.buttons:
            button.checkHover(pygame.mouse.get_pos())
            button.draw(self.WIN)

    def setApp(self, appName: str) -> None:
        '''Sets the app for visualization'''
        self.clearScreen(update=True)
        exec(f"from {appName} import App\nself.app: App = App(self.WIN)")
    
    def quitApp(self) -> None:
        self.app.quit()
    
    def quit(self) -> None:
        pygame.quit()
    
    def mainloop(self) -> None:
        while self.run:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.run = False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                self.run = False
                    case pygame.MOUSEBUTTONDOWN:
                        for b in self.buttons:
                            if b.checkPress():
                                break

            # Starting the app if it is set
            if self.app is not None:
                self.run = self.app.mainloop()
                self.app = None
            
            self.draw()
        
        self.quit()

if __name__ == "__main__":
    mainApp: MainApp = MainApp()
    mainApp.mainloop()