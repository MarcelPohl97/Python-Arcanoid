from tkinter import *
import time
import random
import pygame





def game_breaker():

    gameroot = Tk()
    gameroot.title("Game Root")
    gameroot.resizable(0,0)
    gameroot.wm_attributes("-topmost", 1)
    gamerootCanvas = Canvas(gameroot, width= 665.9, height=500, bd=0, highlightthickness=0)
    gameroot_Background = PhotoImage(file="background.png")
    gamerootCanvas.create_image(250,250,image=gameroot_Background)
    gamerootCanvas.pack()
    gamerootCanvas.update()

    class Ball:
        def __init__(self, gamerootCanvas, paddle, bricks, color):
            self.paddle = paddle
            self.bricks = bricks
            self.pygame = pygame.init()
            self.gamerootCanvas = gamerootCanvas
            self.imageball = PhotoImage(file="ball.png")
            self.id = gamerootCanvas.create_image(0,0,image=self.imageball)
            self.gamerootCanvas.move(self.id, 350, 250)
            self.loose_text = gamerootCanvas.create_text(-50, -50, text="Loose", font=("Arial, 40"), fill="#00d4ff")
            self.start = [-3, -2, -1, 1, 2, 3]
            self.random1 = random.choice(self.start)
            self.x = self.random1
            self.y = 2
            self.hit_bottom = False
            self.gamerootCanvas_height = gamerootCanvas.winfo_height()
            self.gamerootCanvas_width = gamerootCanvas.winfo_width()
            self.image_height = self.imageball.height()
            self.image_width = self.imageball.width()
            self.hit = 0



        def play_pong_sound(self):
            pygame.mixer.music.load("ponghit.mp3")
            pygame.mixer.music.play()

        def play_brick_sound(self):
            pygame.mixer.music.load("bricks.mp3")
            pygame.mixer.music.play()

        def play_win_sound(self):
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play()

        def play_collision_sound(self):
            pygame.mixer.music.load("ballcollision.wav")
            pygame.mixer.music.play()

        def play_loose_sound(self):
            pygame.mixer.music.load("loose.mp3")
            pygame.mixer.music.play()





        def loose_game(self):
            self.gamerootCanvas.move(self.loose_text, 400, 300)

        def check_ball(self):

            self.gamerootCanvas.move(self.id, self.x, self.y)
            pos = self.gamerootCanvas.bbox(self.id)
            if pos[0] <= 0:
                self.play_collision_sound()
                self.x = 2
            elif pos[2] >= self.gamerootCanvas_width:
                self.play_collision_sound()
                self.x = -2
            elif pos[1] <= 0:
                self.play_collision_sound()
                self.y = 2
            elif pos[3] >= self.gamerootCanvas_height:
                self.play_loose_sound()
                self.hit_bottom = True
                self.loose_game()
                self.y = -2
            elif self.hit_paddle(pos) == True:
                self.play_pong_sound()
                self.y = -4
            elif self.brick_hit(pos):
                self.play_brick_sound()
                self.y = 2

        def hit_paddle(self, pos):
            paddle_pos = self.gamerootCanvas.bbox(self.paddle.id)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:

                    self.play_pong_sound()
                    return True
            return False

        def brick_hit(self, pos):
            for brick_line in self.bricks:
                for brick in brick_line:
                    brick_pos = self.gamerootCanvas.bbox(brick.id)
                    # print(brick_pos)
                    try:
                        if pos[1] >= brick_pos[1] and pos[1] <= brick_pos[3]:
                            if pos[0] >= brick_pos[0] and pos[0] <= brick_pos[2]:
                                self.gamerootCanvas.delete(brick.id)




                                return True
                    except:
                        continue
            return False

    class Paddle:
        def __init__(self, gamerootCanvas, color):
            self.gamerootCanvas = gamerootCanvas
            self.paddleimage = PhotoImage(file="paddle.png")
            self.id = gamerootCanvas.create_image(0,0,image=self.paddleimage)
            self.gamerootCanvas.move(self.id, 250, 400)
            self.x = 2
            self.y = 0
            self.gamerootCanvas_height = gamerootCanvas.winfo_height()
            self.gamerootCanvas_width = gamerootCanvas.winfo_width()
            self.gamerootCanvas.bind_all("<KeyPress-Left>", self.turn_left)
            self.gamerootCanvas.bind_all("<KeyPress-Right>", self.turn_right)

        def check_paddle(self):
            self.gamerootCanvas.move(self.id, self.x, self.y)
            pos = self.gamerootCanvas.bbox(self.id)

            if pos[0] <= 0:
                self.x = 5
            if pos[2] >= self.gamerootCanvas_width:
                self.x = -5

        def turn_left(self, evt):
            self.x = -5

        def turn_right(self, evt):
            self.x = 5

    class Brick:
        def __init__(self, gamerootCanvas, color):
            self.gamerootCanvas = gamerootCanvas
            self.photobrick = PhotoImage(file="brick3.png")
            self.id = gamerootCanvas.create_image(35,20,image=self.photobrick)

        def check_brick(self):
            pos = self.gamerootCanvas.coords(self.id)

    def generate_bricks():
        global bricks
        bricks = []
        for i in range(0, 5):
            b = []
            for j in range(0, 11):
                ObjectBrick = Brick(gamerootCanvas, None)
                b.append(ObjectBrick)
            bricks.append(b)

        for i in range(0, 5):
            for j in range(0, 11):
                gamerootCanvas.move(bricks[i][j].id, 60 * j, 40 * i)

    generate_bricks()

    ObjectBrick = Brick(gamerootCanvas, "red")
    paddle = Paddle(gamerootCanvas, "#00d4ff")
    ball = Ball(gamerootCanvas, paddle, bricks, "Red")

    while True:
        ObjectBrick.check_brick()
        paddle.check_paddle()
        ball.check_ball()

        gameroot.update_idletasks()

        gameroot.update()
        time.sleep(0.01)

        if ball.hit_bottom == True:
            ball.loose_game()
            time.sleep(5)
            gameroot.destroy()

game_breaker()