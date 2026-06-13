import sys
import random
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# --- CONSTANTS & CONFIG ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (34, 139, 34)
YELLOW = (240, 230, 140)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
DARK_BLUE = (10, 20, 40)
GOLD = (255, 215, 0)
PURPLE = (147, 112, 219)

# --- GAME DATA ---
CAR_DEALER = [
    {"name": "Rusty Sedan", "speed": 4, "color": YELLOW, "price": 0},
    {"name": "Yellow Cab Pro", "speed": 6, "color": GOLD, "price": 150},
    {"name": "Electric Taxi", "speed": 8, "color": BLUE, "price": 500},
    {"name": "Supercar Taxi", "speed": 11, "color": PURPLE, "price": 1500},
]

HOUSE_MARKET = [
    {"name": "None", "price": 0},
    {"name": "Suburban Apartment", "price": 300},
    {"name": "Downtown Condo", "price": 1000},
    {"name": "Luxury Mansion", "price": 3000},
]


# --- CLASSES ---
class Taxi(pygame.sprite.Sprite):

    def __init__(self, stats):
        super().__init__()
        self.stats = stats
        self.image = pygame.Surface((40, 25))
        self.image.fill(stats["color"])
        # Add a little taxi sign detail
        pygame.draw.rect(self.image, (0, 0, 0), (12, 0, 16, 4))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.speed = stats["speed"]

    def update(self, keys):
        # Grid boundaries (Stay on the paved roads/city center area)
        if keys[pygame.K_LEFT] and self.rect.left > 50:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH - 50:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 120:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 50:
            self.rect.y += self.speed


class Passenger(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        # Random position on roads
        self.rect = self.image.get_rect(
            center=(random.randint(100, 700), random.randint(150, 500))
        )


class DropoffZone(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Translucent blue square
        pygame.draw.rect(
            self.image, (30, 144, 255, 150), (0, 0, 50, 50), border_radius=5
        )
        self.rect = self.image.get_rect(
            center=(random.randint(100, 700), random.randint(150, 500))
        )


# --- MAIN GAME CLASS ---
class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Taxi Tycoon: City Driver")
        self.clock = pygame.clock.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)

        # Progression State
        self.money = 0
        self.current_car_idx = 0
        self.current_house_idx = 0

        # Passenger State
        self.has_passenger = False
        self.fare_value = 0

        # Sprite Groups
        self.taxi_group = pygame.sprite.GroupSingle()
        self.passenger_group = pygame.sprite.GroupSingle()
        self.dropoff_group = pygame.sprite.GroupSingle()

        # Init First Elements
        self.spawn_taxi()
        self.spawn_passenger()

    def spawn_taxi(self):
        self.taxi = Taxi(CAR_DEALER[self.current_car_idx])
        self.taxi_group.add(self.taxi)

    def spawn_passenger(self):
        self.passenger = Passenger()
        self.passenger_group.add(self.passenger)
        # Cash value depends on how fast your current car is (incentive to upgrade!)
        self.fare_value = random.randint(40, 80) + (self.taxi.speed * 5)

    def spawn_dropoff(self):
        self.dropoff = DropoffZone()
        self.dropoff_group.add(self.dropoff)

    def handle_collisions(self):
        # Pick up passenger
        if (
            not self.has_passenger
            and pygame.sprite.spritecollideinside
            and pygame.sprite.collide_rect(self.taxi, self.passenger)
        ):
            self.has_passenger = True
            self.passenger_group.empty()
            self.spawn_dropoff()

        # Drop off passenger
        if self.has_passenger and pygame.sprite.collide_rect(
            self.taxi, self.dropoff
        ):
            self.money += self.fare_value
            self.has_passenger = False
            self.dropoff_group.empty()
            self.spawn_passenger()

    def draw_ui(self):
        # Background Header Panel
        pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, WHITE, (0, 100), (SCREEN_WIDTH, 100), 2)

        # Text Renderers
        money_txt = self.title_font.render(
            f"Wallet: ${self.money}", True, GOLD
        )
        car_txt = self.font.render(
            f"Vehicle: {CAR_DEALER[self.current_car_idx]['name']}", True, WHITE
        )
        house_txt = self.font.render(
            f"Property: {HOUSE_MARKET[self.current_house_idx]['name']}",
            True,
            WHITE,
        )

        self.screen.blit(money_txt, (20, 20))
        self.screen.blit(car_txt, (20, 55))
        self.screen.blit(house_txt, (250, 55))

        # Instructions / Context UI
        if not self.has_passenger:
            status_txt = self.font.render(
                f"Status: Search for the RED passenger! (Fare: ${self.fare_value})",
                True,
                YELLOW,
            )
        else:
            status_txt = self.font.render(
                "Status: Drive to the BLUE drop-off zone!", True, BLUE
            )
        self.screen.blit(status_txt, (250, 20))

        # Shop Menus (Right Side Header)
        shop_header = self.font.render("UPGRADES (Press Key):", True, WHITE)
        self.screen.blit(shop_header, (540, 10))

        # Show next car option
        if self.current_car_idx < len(CAR_DEALER) - 1:
            next_car = CAR_DEALER[self.current_car_idx + 1]
            car_shop = self.font.render(
                f"[C] Next Car: ${next_car['price']}", True, GREEN
            )
        else:
            car_shop = self.font.render("Cars Maxed Out!", True, WHITE)

        # Show next house option
        if self.current_house_idx < len(HOUSE_MARKET) - 1:
            next_house = HOUSE_MARKET[self.current_house_idx + 1]
            house_shop = self.font.render(
                f"[H] Next House: ${next_house['price']}", True, GREEN
            )
        else:
            house_shop = self.font.render("Real Estate Maxed!", True, WHITE)

        self.screen.blit(car_shop, (540, 40))
        self.screen.blit(house_shop, (540, 65))

    def buy_car(self):
        if self.current_car_idx < len(CAR_DEALER) - 1:
            next_car = CAR_DEALER[self.current_car_idx + 1]
            if self.money >= next_car["price"]:
                self.money -= next_car["price"]
                self.current_car_idx += 1
                self.spawn_taxi()  # Reload taxi with new stats

    def buy_house(self):
        if self.current_house_idx < len(HOUSE_MARKET) - 1:
            next_house = HOUSE_MARKET[self.current_house_idx + 1]
            if self.money >= next_house["price"]:
                self.money -= next_house["price"]
                self.current_house_idx += 1

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            # --- EVENT HANDLING ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.buy_car()
                    if event.key == pygame.K_h:
                        self.buy_house()

            # --- UPDATE ---
            keys = pygame.key.get_pressed()
            self.taxi_group.update(keys)
            self.handle_collisions()

            # --- DRAW ---
            self.screen.fill(GREEN)  # Grass background

            # Draw simple city roads grid layout
            pygame.draw.rect(
                self.screen, GRAY, (50, 120, SCREEN_WIDTH - 100, 430)
            )

            # Draw game objects
            self.dropoff_group.draw(self.screen)
            self.passenger_group.draw(self.screen)
            self.taxi_group.draw(self.screen)

            # Draw HUD Overlays
            self.draw_ui()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
