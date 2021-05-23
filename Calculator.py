import pygame, sys
import pygame.time
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Window dimensions
windowWidth = 400
windowHeight = 600
windowBorder = 20

surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('High Precision Calculator')

mousePosition = None
anim_delay = 10

# Buttons library
buttons = []
click_sound = pygame.mixer.Sound('assets/sounds/Digital_Watch02.ogg')
buttonSize = 50

# Calculation Variables
choice = 0
plus = 0

# LCD display variables and list
readout = str(0)
lcd_view = []
# readout cannot be more than 9 numbers.

# Calculator title Brand Name
label_font = pygame.font.Font("assets/fonts/label.ttf", 30)
label_text = label_font.render("SPASSIO", True, (200, 200, 200))
# Calculator display text
calc_font = pygame.font.Font("assets/fonts/calculate.ttf", 70)
calc_type = calc_font.render(readout, True, (0, 200, 50))


# button class
class button:
    # Key slots
    slots = [(70, 260, "9"), (130, 260, "8"), (190, 260, "7"),
             (70, 320, "6"), (130, 320, "5"), (190, 320, "4"),
             (70, 380, "3"), (130, 380, "2"), (190, 380, "1"),
             (130, 440, "0"), (260, 200, "/"), (260, 260, "x"),
             (260, 320, "-"), (260, 380, "+"), (260, 440, "="),
             (70, 200, "C"), (190, 440, "."), (130, 200, "√"),
             (190, 200, "%")
             ]
    slot = 0
    x = 0
    y = 0
    start_x = 0
    start_y = 0
    key_value = None

    width = 50
    height = 50

    def draw(self, surface):

        pygame.draw.rect(surface, (40, 40, 40), (self.x, self.y, button.width, button.height))
        pygame.draw.rect(surface, (100, 100, 100), (self.x + 2, self.y + 2, button.width - 4, button.height - 4))
        pygame.draw.circle(surface, (80, 90, 90), (self.x + (button.width // 2), self.y + (button.height // 2)), (button.width - 8) // 2, 0)
        face = pygame.font.SysFont(None, 30)
        face_num = face.render(str(self.key_value), True, (0, 0, 0))
        surface.blit(face_num, (self.x + 20, self.y + 16))

    # Mouse Click
    def click(self):
        # Choice reflects the previous operation.
        # 1 = addition
        # 2 = subtraction
        # 3 = multiplication
        # 4 = division
        # 5 = square root
        global mousePosition, readout, plus, choice, buttonSize

        if mousePosition[0] > self.x and mousePosition[0] < self.x + button.width:
            if mousePosition[1] > self.y and mousePosition[1] < self.y + button.height:
                click_sound.set_volume(1.0)
                click_sound.play()
                self.x += 1
                self.y += 2
                if self.key_value == "C":  # button number 15 is "Clear" button
                    choice = 0
                    plus = 0
                    clear_lcd()
                elif self.key_value == "+":  # addition
                    function_check()
                    choice = 1
                    clear_lcd()
                    readout = str(plus)

                elif self.key_value == "-":  # subtraction
                    function_check()
                    choice = 2
                    clear_lcd()
                    readout = str(plus)

                elif self.key_value == "x":  # multiplication
                    function_check()
                    choice = 3
                    clear_lcd()
                    readout = str(plus)

                elif self.key_value == "/":  # division
                    function_check()
                    choice = 4
                    clear_lcd()
                    readout = str(plus)

                elif self.key_value == "=":  # Equals
                    function_check()
                    choice = 0
                    clear_lcd()
                    readout = str(plus)

                elif self.key_value == "√": # Root
                    choice = 5
                    clear_lcd()
                    readout = str(plus)

                elif len(lcd_view) < 9:
                    if self.key_value == ".": # Point
                        if "." not in lcd_view:
                            lcd_view.append(str(self.key_value))
                    else:
                        lcd_view.append(str(self.key_value))

    def button_reset(self):
        self.x = self.start_x
        self.y = self.start_y

    def __init__(self, slot):
        self.slot = slot
        self.x = self.slots[slot][0]
        self.y = self.slots[slot][1]
        self.start_x = self.x
        self.start_y = self.y
        self.key_value = self.slots[slot][2]


def draw_buttons():
    for idx, button in enumerate(buttons):
        button.draw(surface)


def function_check():
    global plus, choice, readout

    if readout == "ERROR":
        readout = 0

    if choice == 0:
        plus = float(readout)
    elif choice == 1:
        plus += float(readout)
    elif choice == 2:
        plus = plus - float(readout)
    elif choice == 3:
        plus = plus * float(readout)
    elif choice == 4:
        plus = plus / float(readout)
    elif choice == 5:
        plus = (float(readout)) ** 0.5
    if (plus - int(plus)) == 0:
        plus = int(plus)


def calcBackground():
    # Calculator main background
    pygame.draw.rect(surface, (40, 40, 40), (windowBorder, windowBorder, (windowWidth - (windowBorder * 2)), (windowHeight - (windowBorder * 2))))
    pygame.draw.rect(surface, (80, 80, 80), (windowBorder + 5, windowBorder + 5, (windowWidth - (windowBorder * 2 + 10)), (windowHeight - (windowBorder * 2 + 10))))
    pygame.draw.rect(surface, (40, 40, 40), (windowBorder + 25, windowBorder + 35, (windowWidth - (windowBorder * 2 + 50)), 75))
    pygame.draw.rect(surface, (0, 65, 50), (windowBorder + 30, windowBorder + 40, (windowWidth - (windowBorder * 2 + 60)), 65))
    pygame.draw.rect(surface, (40, 40, 40), (windowBorder + 25, windowBorder + 120, (windowWidth - (windowBorder * 2 + 50)), 4))
    # Calculator Title
    surface.blit(label_text, (windowBorder + 30, windowBorder + 4))


def calcReadout():
    # Show output on the LCD screen.

    global readout

    if len(lcd_view) >= 1:  # This allows "0" to be shown at start
        conCat = "".join(lcd_view)
        readout = conCat
    # If the above is not in place, the readout at the beginning is blank due to it printing the list instead of 0.

    if len(readout) > 9:
        readout = readout[0:9] # print only first nine characters in the string
    calc_type = calc_font.render(readout, True, (0, 200, 50))
    textWidth = calc_type.get_rect().size
    surface.blit(calc_type, ((windowWidth - (windowBorder * 2 + 15 + textWidth[0])), windowBorder + 25))


def clear_lcd():
    global readout
    lcd_view.clear()
    readout = str(0)


def quitGame():
    pygame.quit()
    sys.exit()


# Add individual buttons to the Buttons list (instance buttons)
for make in range(len(button.slots)):
    buttons.append(button(make))

# Main loop
while True:

    surface.fill((50, 0, 0))
    mousePosition = pygame.mouse.get_pos()

    for event in GAME_EVENTS.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, button in enumerate(buttons):
                button.click()
        if event.type == pygame.MOUSEBUTTONUP:
            for idx, button in enumerate(buttons):
                button.button_reset()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    calcBackground()
    draw_buttons()
    calcReadout()
    pygame.display.update()
