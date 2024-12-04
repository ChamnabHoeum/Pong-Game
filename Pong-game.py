import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
BALL_SPEED = [5, 5]
PADDLE_SPEED = 10
SCORE_LIMIT = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (169, 169, 169)
PURPLE = (138, 43, 226)
GREEN = (0, 128, 0)
PINK = (255, 105, 180)

class Paddle:
    def __init__(self, x, y, width, height, player_name):
        self.rect = pygame.Rect(x, y, width, height)
        self.player_name = player_name

    def move(self, dy):
        if 0 <= self.rect.top + dy <= HEIGHT - self.rect.height:
            self.rect.move_ip(0, dy)

class Ball:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.dx, self.dy = random.choice([(-5, -5), (-5, 5), (5, -5), (5, 5)])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.dx *= -1

    def check_boundary(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    def check_score(self):
        if self.rect.left <= 0:
            return 2
        if self.rect.right >= WIDTH:
            return 1
        return 0

    def increase_speed(self):
        # Increase speed by 10% each time
        self.dx *= 1.1
        self.dy *= 1.1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.font = pygame.font.Font(None, 36)
        self.paddle1 = Paddle(50, HEIGHT // 2 - 50, 15, 100, "Player 1")
        self.paddle2 = Paddle(WIDTH - 50 - 10, HEIGHT // 2 - 50, 15, 100, "Player 2")
        self.ball = Ball(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 20)
        self.score1 = 0
        self.score2 = 0
        self.start_time = pygame.time.get_ticks()  # Start time to track the duration of the game
        self.speed_increase_time = self.start_time  # Time to track when to increase ball speed

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            self.paddle1.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            self.paddle2.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            self.paddle2.move(PADDLE_SPEED)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.paddle1, self.paddle2)
        self.ball.check_boundary()
        score = self.ball.check_score()
        if score == 1:
            self.score1 += 1
            self.reset_ball()
        elif score == 2:
            self.score2 += 1
            self.reset_ball()

        #increase ball speed
        elapsed_time = (pygame.time.get_ticks() - self.speed_increase_time) / 1000  # Time in seconds
        if elapsed_time >= 15:  # If 15 seconds passed
            self.ball.increase_speed()
            self.speed_increase_time = pygame.time.get_ticks()  # Reset the timer for the next speed increase

    def reset_ball(self):
        self.ball = Ball(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 20)

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, GREY, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 2)
        pygame.draw.rect(self.screen, RED, self.paddle1.rect)
        pygame.draw.rect(self.screen, BLUE, self.paddle2.rect)
        pygame.draw.ellipse(self.screen, WHITE, self.ball.rect)
        score_display = self.font.render(f"{self.score1}    {self.score2}", True, WHITE)
        self.screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))
        player1_name_text = self.font.render(self.paddle1.player_name, True, WHITE)
        self.screen.blit(player1_name_text, [10, 10])

        player2_name_text = self.font.render(self.paddle2.player_name, True, WHITE)
        self.screen.blit(player2_name_text, [WIDTH - player2_name_text.get_width() - 10, 10])
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(PURPLE)
        title_font = pygame.font.Font(None, 100)
        title_text = title_font.render("PONG GAME", True, GREEN)
        start_font = pygame.font.Font(None, 35)
        start_text = start_font.render("Press SPACE to start", True, WHITE)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 230))
        self.screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 330))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def show_game_over(self, winner):
        self.screen.fill(PURPLE)
        game_over_font = pygame.font.Font(None, 80)
        winner_text = game_over_font.render(f"Player {winner} wins!", True, PINK)
        restart_font = pygame.font.Font(None, 35)
        restart_text = restart_font.render("Press SPACE to restart", True, WHITE)
        self.screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, 230))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 330))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def run(self):
        clock = pygame.time.Clock()
        self.show_start_screen()
        while True:
            self.handle_input()
            self.update()
            self.draw()
            if self.score1 >= SCORE_LIMIT or self.score2 >= SCORE_LIMIT:
                winner = 1 if self.score1 >= SCORE_LIMIT else 2
                self.show_game_over(winner)
                self.reset_game()
                self.show_start_screen()
            clock.tick(60)

    def reset_game(self):
        self.score1 = 0
        self.score2 = 0
        self.paddle1 = Paddle(50, HEIGHT // 2 - 50, 15, 100, "Player 1")
        self.paddle2 = Paddle(WIDTH - 50 - 10, HEIGHT // 2 - 50, 15, 100, "Player 2")
        self.ball = Ball(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 20)
        self.start_time = pygame.time.get_ticks()  # Reset the start time
        self.speed_increase_time = self.start_time  # Reset the speed increase timer


if __name__ == "__main__":
    game = Game()
    game.run()
