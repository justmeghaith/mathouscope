import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton, DirectEntry, DirectFrame
from panda3d.core import TextNode, Vec3, WindowProperties

class GTALiteGame(ShowBase):
    def __init__(self):
        super().__init__()
        
        # --- GAME STATE ---
        self.loney = 500  # Currency named Loney
        self.is_married = False
        self.has_kids = False
        self.current_outfit = "Default Rags"
        self.current_shoes = "Old Sneakers"
        self.selected_location = "Liberty City"
        self.current_car = "None (On Foot)"
        self.is_flying = False
        self.is_driving = False
        
        # 21 Cars list - Lamborghini is explicitly the crown jewel
        self.car_list = [
            "Lamborghini Aventador (BEST)", "Ferrari 488", "Porsche 911", 
            "Bugatti Chiron", "McLaren P1", "Aston Martin DB11", "Nissan GT-R",
            "Toyota Supra", "Ford Mustang", "Chevrolet Camaro", "Dodge Charger",
            "BMW M4", "Audi R8", "Mercedes AMG GT", "Tesla Model S", 
            "Honda Civic Type R", "Volkswagen Golf GTI", "Jeep Wrangler",
            "Range Rover", "Subaru WRX STI", "Mazda RX-7"
        ]
        
        # Setup window properties
        props = WindowProperties()
        props.setTitle("GTA V Lite Prototype")
        props.setSize(1024, 768)
        self.win.requestProperties(props)
        
        # Initialize UI layers
        self.menu_frame = None
        self.hud_frame = None
        self.customizer_frame = None
        self.admin_entry = None
        
        # Camera starting position
        self.disableMouse()
        self.camera.setPos(0, -20, 3)
        
        # Start at Main Menu
        self.build_main_menu()

    # --- UI HELPERS ---
    def clear_ui(self):
        if self.menu_frame: self.menu_frame.destroy()
        if self.hud_frame: self.hud_frame.destroy()
        if self.customizer_frame: self.customizer_frame.destroy()

    # --- MAIN MENU ---
    def build_main_menu(self):
        self.clear_ui()
        self.menu_frame = DirectFrame(frameColor=(0.1, 0.1, 0.15, 1), frameSize=(-1.5, 1.5, -1, 1))
        
        # Title
        OnscreenText(text="GRAND THEFT LONEY V", pos=(0, 0.7), scale=0.12, 
                     fg=(1, 0.8, 0, 1), align=TextNode.ACenter, parent=self.menu_frame)
        
        # Mode Selection
        DirectButton(text="OFFLINE MODE", pos=(-0.4, 0.4, 0), scale=0.08, 
                     command=self.open_customizer, parent=self.menu_frame)
        DirectButton(text="ONLINE MODE (Connecting...)", pos=(0.4, 0.4, 0), scale=0.08, 
                     command=self.open_customizer, parent=self.menu_frame)
        
        # Controls Box
        controls_text = (
            "--- CONTROLS ---\n"
            "WASD / Arrows : Move & Drive\n"
            "T : Steal Nearby Vehicle\n"
            "E : Eat Street Food ($10)\n"
            "M : Propose / Get Married ($200)\n"
            "K : Have Kids (Spawn NPC)\n"
            "` (Tilde) : Open Admin Command Console"
        )
        OnscreenText(text=controls_text, pos=(-0.8, -0.1), scale=0.05, 
                     fg=(1, 1, 1, 1), align=TextNode.ALeft, parent=self.menu_frame)
        
        # World Drop locations
        OnscreenText(text="Select Drop Destination:", pos=(0.5, -0.1), scale=0.05, fg=(0.7, 0.7, 1, 1), parent=self.menu_frame)
        self.loc_btn = DirectButton(text=f"Location: {self.selected_location}", pos=(0.5, -0.25, 0), scale=0.06, 
                                    command=self.toggle_location, parent=self.menu_frame)

    def toggle_location(self):
        locations = ["Liberty City", "Los Santos", "Vice City", "Tokyo", "London", "Paris"]
        idx = (locations.index(self.selected_location) + 1) % len(locations)
        self.selected_location = locations[idx]
        self.loc_btn["text"] = f"Location: {self.selected_location}"

    # --- CHARACTER CUSTOMIZATION ---
    def open_customizer(self):
        self.clear_ui()
        self.customizer_frame = DirectFrame(frameColor=(0.15, 0.15, 0.2, 1), frameSize=(-1.5, 1.5, -1, 1))
        
        self.cust_title = OnscreenText(text=f"Character Customizer | Wallet: ${self.loney} Loney", 
                                       pos=(0, 0.8), scale=0.08, fg=(1, 1, 1, 1), parent=self.customizer_frame)
        
        # Clothes options
        OnscreenText(text="Select Torso Wear:", pos=(-0.5, 0.4), scale=0.05, fg=(1,1,1,1), parent=self.customizer_frame)
        DirectButton(text="Leather Jacket ($80)", pos=(-0.5, 0.25, 0), scale=0.06, command=lambda: self.buy_item("clothes", "Leather Jacket", 80), parent=self.customizer_frame)
        DirectButton(text="Designer Hoodie ($150)", pos=(-0.5, 0.1, 0), scale=0.06, command=lambda: self.buy_item("clothes", "Designer Hoodie", 150), parent=self.customizer_frame)
        
        # Shoes options
        OnscreenText(text="Select Footwear:", pos=(0.5, 0.4), scale=0.05, fg=(1,1,1,1), parent=self.customizer_frame)
        DirectButton(text="Running Kicks ($50)", pos=(0.5, 0.25, 0), scale=0.06, command=lambda: self.buy_item("shoes", "Running Kicks", 50), parent=self.customizer_frame)
        DirectButton(text="Luxury Hype Shoes ($300)", pos=(0.5, 0.1, 0), scale=0.06, command=lambda: self.buy_item("shoes", "Luxury Hype Shoes", 300), parent=self.customizer_frame)
        
        # Outfit Status display
        self.status_outfit = OnscreenText(text=f"Current Outfit: {self.current_outfit} | Shoes: {self.current_shoes}", 
                                          pos=(0, -0.3), scale=0.05, fg=(0.8, 1, 0.8, 1), parent=self.customizer_frame)
        
        # Spawn Button
        DirectButton(text="SPAWN INTO WORLD", pos=(0, -0.6, 0), scale=0.08, bg=(0.2, 0.6, 0.2, 1),
                     command=self.start_world_game, parent=self.customizer_frame)

    def buy_item(self, item_type, name, price):
        if self.loney >= price:
            self.loney -= price
            if item_type == "clothes": self.current_outfit = name
            else: self.current_shoes = name
            self.cust_title["text"] = f"Character Customizer | Wallet: ${self.loney} Loney"
            self.status_outfit["text"] = f"Current Outfit: {self.current_outfit} | Shoes: {self.current_shoes}"
        else:
            self.cust_title["text"] = "INSUFFICIENT LONEY SYSTEM ERROR!"

    # --- 3D WORLD PLAY ---
    def start_world_game(self):
        self.clear_ui()
        
        # Build 3D World Geometry
        # Spawn basic environment shapes dynamically
        self.environment = self.loader.loadModel("models/box")
        self.environment.reparentTo(self.render)
        self.environment.setScale(60, 60, 0.1)
        self.environment.setPos(0, 0, 0)
        self.environment.setColor(0.2, 0.3, 0.2, 1) # Green terrain ground
        
        # Render a basic mock 3D city skyscraper building structure block
        self.building = self.loader.loadModel("models/box")
        self.building.reparentTo(self.render)
        self.building.setScale(5, 5, 15)
        self.building.setPos(10, 30, 0)
        self.building.setColor(0.4, 0.4, 0.4, 1)

        # Build functional HUD
        self.hud_frame = DirectFrame(frameColor=(0,0,0,0.4), frameSize=(-1, 1, 0.7, 1), pos=(0,0,0))
        self.hud_money = OnscreenText(text=f"Loney: ${self.loney}", pos=(-1.2, 0.9), scale=0.05, fg=(0.2, 1, 0.2, 1), align=TextNode.ALeft)
        self.hud_status = OnscreenText(text=f"Location: {self.selected_location} | Car: {self.current_car}", pos=(-1.2, 0.83), scale=0.04, fg=(1,1,1,1), align=TextNode.ALeft)
        self.hud_social = OnscreenText(text="Status: Single", pos=(-1.2, 0.76), scale=0.04, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft)
        self.system_feed = OnscreenText(text="Welcome! Use Arrow Keys to move. Press ` to enter Admin Commands.", pos=(0, -0.9), scale=0.045, fg=(1,1,0,1), align=TextNode.ACenter)

        # Bind Interaction Keys
        self.accept("e", self.game_action_eat)
        self.accept("t", self.game_action_steal_car)
        self.accept("m", self.game_action_marry)
        self.accept("k", self.game_action_have_kids)
        
        # Bind Admin Console Trigger Key
        self.accept("`", self.toggle_admin_console)
        
        # Movement loops
        self.keys = {"left": 0, "right": 0, "forward": 0, "back": 0}
        self.accept("arrow_left", self.set_key, ["left", 1])
        self.accept("arrow_left-up", self.set_key, ["left", 0])
        self.accept("arrow_right", self.set_key, ["right", 1])
        self.accept("arrow_right-up", self.set_key, ["right", 0])
        self.accept("arrow_up", self.set_key, ["forward", 1])
        self.accept("arrow_up-up", self.set_key, ["forward", 0])
        self.accept("arrow_down", self.set_key, ["back", 1])
        self.accept("arrow_down-up", self.set_key, ["back", 0])
        
        self.taskMgr.add(self.move_loop, "MoveLoopTask")

    def set_key(self, key, value):
        self.keys[key] = value

    def move_loop(self, task):
        # Determine speed factors depending on flying or car driving states
        speed = 15.0 if self.is_driving else 5.0
        if self.is_flying: speed = 30.0
        
        dt = globalClock.getDt()
        
        if self.keys["forward"]: self.camera.setY(self.camera, speed * dt)
        if self.keys["back"]: self.camera.setY(self.camera, -speed * dt)
        if self.keys["left"]: self.camera.setX(self.camera, -speed * dt)
        if self.keys["right"]: self.camera.setX(self.camera, speed * dt)
        
        return task.cont

    # --- ACTIONS ---
    def game_action_eat(self):
        if self.loney >= 10:
            self.loney -= 10
            self.system_feed["text"] = "You bought a street taco and refueled your health meter!"
            self.update_hud()
        else:
            self.system_feed["text"] = "Not enough Loney to buy food!"

    def game_action_steal_car(self):
        if not self.is_driving:
            self.is_driving = True
            # Randomly select from the list, with special premium scaling if it picks Lamborghini
            chosen = random.choice(self.car_list)
            self.current_car = chosen
            if "Lamborghini" in chosen:
                self.system_feed["text"] = f"GRAND THEFT AUTO! You hijacked a {chosen}! Maximum speeds unlocked!"
            else:
                self.system_feed["text"] = f"Grand Theft Auto! You jacked a civilian {chosen}."
        else:
            self.is_driving = False
            self.system_feed["text"] = f"Exited your {self.current_car} and dropped down safely on foot."
            self.current_car = "None (On Foot)"
        self.update_hud()

    def game_action_marry(self):
        if not self.is_married:
            if self.loney >= 200:
                self.loney -= 200
                self.is_married = True
                self.system_feed["text"] = "Wedding bells chime! You are officially married to an NPC!"
                self.update_hud()
            else:
                self.system_feed["text"] = "Marriage licensing weddings cost $200 Loney."
        else:
            self.system_feed["text"] = "You are already committed to your spouse."

    def game_action_have_kids(self):
        if not self.is_married:
            self.system_feed["text"] = "Get married first before raising kids!"
            return
        self.has_kids = True
        self.system_feed["text"] = "NPC Toddler spawned at home! Your legacy grows."
        self.update_hud()

    def update_hud(self):
        self.hud_money["text"] = f"Loney: ${self.loney}"
        self.hud_status["text"] = f"Location: {self.selected_location} | Car: {self.current_car}"
        
        social = "Single"
        if self.is_married: social = "Married💍"
        if self.has_kids: social += " & Has Kids👶"
        self.hud_social["text"] = f"Status: {social}"

    # --- ADMIN CHEAT ENGINE CONSOLE ---
    def toggle_admin_console(self):
        if self.admin_entry:
            self.admin_entry.destroy()
            self.admin_entry = None
        else:
            self.system_feed["text"] = "Console Ready. Type /loney or /fly and hit enter."
            self.admin_entry = DirectEntry(text="", scale=0.05, pos=(-0.5, 0, -0.7),
                                           numLines=1, command=self.execute_admin_command,
                                           focus=1, focusInCommand=None)

    def execute_admin_command(self, cmd_text):
        cmd = cmd_text.strip().lower()
        
        if cmd == "/loney":
            self.loney = float('inf')  # Infinite Loney
            self.system_feed["text"] = "ADMIN CHEAT: Infinite Loney cash reserves granted!"
        elif cmd == "/fly":
            self.is_flying = not self.is_flying
            state = "ENABLED" if self.is_flying else "DISABLED"
            self.system_feed["text"] = f"ADMIN CHEAT: Fly/Noclip mode is now {state}."
        else:
            self.system_feed["text"] = "Unknown Admin script command. Try /loney or /fly."
            
        self.update_hud()
        if self.admin_entry:
            self.admin_entry.destroy()
            self.admin_entry = None

# Run Game Prototype Execution Loop
if __name__ == "__main__":
    game = GTALiteGame()
    game.run()
