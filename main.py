import os
import sys
import math
import random
import pygame
import cv2
from PIL import Image

# ============================================================
# FROM ME TO YOU
# A small RPG-style gift game
# ============================================================

pygame.init()
pygame.mixer.init()

# ------------------------------------------------------------
# WINDOW
# ------------------------------------------------------------

WIDTH = 1200
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FROM ME TO YOU")

clock = pygame.time.Clock()

# ------------------------------------------------------------
# FOLDERS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIC_DIR = os.path.join(BASE_DIR, "music")
VIDEO_DIR = os.path.join(BASE_DIR, "video")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
FONT_DIR = os.path.join(BASE_DIR, "fonts")

# ------------------------------------------------------------
# MUSIC
# ------------------------------------------------------------

MUSIC_START_SECONDS = 45

MUSIC = {
    "menu": os.path.join(
        MUSIC_DIR,
        "everybody_wants_to_rule_the_world.mp3"
    ),

    "breakfast": os.path.join(
        MUSIC_DIR,
        "pink_pantheress.mp3"
    ),

    "lunch": os.path.join(
        MUSIC_DIR,
        "a_sky_full_of_stars.mp3"
    ),

    "dinner": os.path.join(
        MUSIC_DIR,
        "somebody_that_i_used_to_know.mp3"
    ),
}

# ------------------------------------------------------------
# MENU SOUND EFFECTS
# ------------------------------------------------------------

HOVER_SOUND_PATH = os.path.join(
    MUSIC_DIR,
    "hover.wav"
)

CLICK_SOUND_PATH = os.path.join(
    MUSIC_DIR,
    "click.wav"
)

hover_sound = None
click_sound = None

try:

    if os.path.exists(HOVER_SOUND_PATH):

        hover_sound = pygame.mixer.Sound(
            HOVER_SOUND_PATH
        )

        hover_sound.set_volume(0.55)

        print(
            "[SOUND] Hover sound loaded."
        )

    else:

        print(
            "[SOUND] hover.wav not found."
        )

except pygame.error as error:

    print(
        "[SOUND ERROR] Could not load hover.wav:"
    )

    print(error)


try:

    if os.path.exists(CLICK_SOUND_PATH):

        click_sound = pygame.mixer.Sound(
            CLICK_SOUND_PATH
        )

        click_sound.set_volume(0.65)

        print(
            "[SOUND] Click sound loaded."
        )

    else:

        print(
            "[SOUND] click.wav not found."
        )

except pygame.error as error:

    print(
        "[SOUND ERROR] Could not load click.wav:"
    )

    print(error)


def play_hover_sound():

    if hover_sound is not None:

        try:
            hover_sound.play()

        except pygame.error:
            pass


def play_click_sound():

    if click_sound is not None:

        try:
            click_sound.play()

        except pygame.error:
            pass


def play_music(scene):

    music_file = MUSIC.get(scene)

    if not music_file:
        return

    if not os.path.exists(music_file):

        print(
            f"[MUSIC ERROR] File not found: "
            f"{music_file}"
        )

        return

    try:

        pygame.mixer.music.stop()

        pygame.mixer.music.load(
            music_file
        )

        pygame.mixer.music.set_volume(
            0.65
        )

        # Start every song at 45 seconds.
        try:

            pygame.mixer.music.play(
                -1,
                start=MUSIC_START_SECONDS
            )

        except TypeError:

            pygame.mixer.music.play(
                -1
            )

            try:

                pygame.mixer.music.set_pos(
                    MUSIC_START_SECONDS
                )

            except pygame.error:

                print(
                    "[MUSIC WARNING] Could not "
                    "seek to 45 seconds."
                )

        print(
            f"[MUSIC] Playing from "
            f"{MUSIC_START_SECONDS}s: "
            f"{os.path.basename(music_file)}"
        )

    except pygame.error as error:

        print(
            "[MUSIC ERROR] Could not play music:"
        )

        print(error)


# ============================================================
# FONTS
# ============================================================

def find_pixel_font():

    if not os.path.exists(FONT_DIR):
        return None

    possible_fonts = []

    for filename in os.listdir(FONT_DIR):

        if filename.lower().endswith(
            (".ttf", ".otf")
        ):

            possible_fonts.append(
                os.path.join(
                    FONT_DIR,
                    filename
                )
            )

    if possible_fonts:

        return possible_fonts[0]

    return None


PIXEL_FONT = find_pixel_font()

if PIXEL_FONT:

    print(
        "[FONT] Using:",
        os.path.basename(PIXEL_FONT)
    )

    TITLE_FONT = pygame.font.Font(
        PIXEL_FONT,
        58
    )

    MENU_FONT = pygame.font.Font(
        PIXEL_FONT,
        31
    )

    SMALL_FONT = pygame.font.Font(
        PIXEL_FONT,
        19
    )

    DINNER_FONT = pygame.font.Font(
        PIXEL_FONT,
        64
    )

else:

    print(
        "[FONT] No custom pixel font found."
    )

    print(
        "[FONT] Using built-in monospace font."
    )

    TITLE_FONT = pygame.font.SysFont(
        "monospace",
        55,
        bold=True
    )

    MENU_FONT = pygame.font.SysFont(
        "monospace",
        30,
        bold=True
    )

    SMALL_FONT = pygame.font.SysFont(
        "monospace",
        19
    )

    DINNER_FONT = pygame.font.SysFont(
        "monospace",
        62,
        bold=True
    )


# ------------------------------------------------------------
# FRIENDLY / CANVA-SANS-LIKE FONT
# ------------------------------------------------------------

BODY_FONT = pygame.font.SysFont(
    "segoeui",
    25
)

ESC_FONT = pygame.font.SysFont(
    "segoeui",
    16
)


# ============================================================
# COLORS
# ============================================================

WHITE = (235, 232, 230)

BLACK = (0, 0, 0)

DARK_BLUE = (12, 17, 30)

# Main menu panel
PANEL_BLUE = (9, 15, 29, 225)
PANEL_BORDER = (37, 44, 63)
PANEL_INNER = (23, 29, 47)

# Main menu title
DARK_PINK = (145, 38, 78)
BLUE = (58, 78, 130)

# Menu colours
MENU_RED = (128, 38, 61)
MENU_SELECTED = (185, 57, 91)

# Arrow
ARROW_PINK = (166, 42, 86)
ARROW_BLUE = (57, 74, 125)

# Meal gradients
MEAL_RED = (185, 48, 65)
MEAL_BLUE = (58, 82, 145)

DESCRIPTION_PINK = (205, 70, 125)
DESCRIPTION_BLUE = (65, 105, 175)

# Border gradient
BORDER_BLUE = (52, 82, 155)
BORDER_RED = (180, 48, 65)

# Dinner
DINNER_BLUE = (65, 95, 175)
DINNER_PINK = (205, 65, 130)


# ============================================================
# VIDEO BACKGROUND
# ============================================================

VIDEO_PATH = os.path.join(
    VIDEO_DIR,
    "background.mp4"
)

video = None
video_width = 0
video_height = 0

if os.path.exists(VIDEO_PATH):

    video = cv2.VideoCapture(
        VIDEO_PATH
    )

    if video.isOpened():

        video_width = int(
            video.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        video_height = int(
            video.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        print(
            "[VIDEO] Main background loaded."
        )

    else:

        print(
            "[VIDEO ERROR] Could not open "
            "background.mp4."
        )

else:

    print(
        "[VIDEO ERROR] background.mp4 "
        "was not found:"
    )

    print(VIDEO_PATH)


def get_video_frame():

    if video is None:
        return None

    success, frame = video.read()

    if not success:

        video.set(
            cv2.CAP_PROP_POS_FRAMES,
            0
        )

        success, frame = video.read()

        if not success:
            return None

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame = cv2.resize(
        frame,
        (WIDTH, HEIGHT)
    )

    surface = pygame.image.frombuffer(
        frame.tobytes(),
        (WIDTH, HEIGHT),
        "RGB"
    )

    return surface.convert()


# ============================================================
# IMAGE LOADING
# ============================================================

def find_image(name):

    extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]

    for extension in extensions:

        path = os.path.join(
            IMAGE_DIR,
            name + extension
        )

        if os.path.exists(path):

            return path

    return None


def load_background(name):

    path = find_image(name)

    if path is None:

        print(
            f"[IMAGE ERROR] Could not find "
            f"{name}.png/.jpg/.jpeg/.webp"
        )

        return None

    try:

        image = pygame.image.load(
            path
        ).convert()

        image = pygame.transform.smoothscale(
            image,
            (WIDTH, HEIGHT)
        )

        print(
            f"[IMAGE] Loaded: "
            f"{os.path.basename(path)}"
        )

        return image

    except pygame.error as error:

        print(
            f"[IMAGE ERROR] Could not load "
            f"{path}"
        )

        print(error)

        return None


breakfast_background = load_background(
    "breakfast"
)

lunch_background = load_background(
    "lunch"
)


# ============================================================
# DINNER GIF
# ============================================================

DINNER_GIF_PATH = os.path.join(
    IMAGE_DIR,
    "dinner.gif"
)

gif_frames = []
gif_durations = []
gif_index = 0
gif_timer = 0


def load_gif():

    global gif_frames
    global gif_durations

    if not os.path.exists(
        DINNER_GIF_PATH
    ):

        print(
            "[GIF ERROR] dinner.gif "
            "was not found:"
        )

        print(DINNER_GIF_PATH)

        return

    try:

        gif = Image.open(
            DINNER_GIF_PATH
        )

        frame_count = gif.n_frames

        for frame_number in range(
            frame_count
        ):

            gif.seek(
                frame_number
            )

            frame = gif.convert(
                "RGB"
            )

            frame = frame.resize(
                (WIDTH, HEIGHT),
                Image.Resampling.LANCZOS
            )

            data = frame.tobytes()

            pygame_frame = (
                pygame.image.fromstring(
                    data,
                    (WIDTH, HEIGHT),
                    "RGB"
                ).convert()
            )

            gif_frames.append(
                pygame_frame
            )

            duration = gif.info.get(
                "duration",
                100
            )

            duration = max(
                20,
                duration
            )

            gif_durations.append(
                duration
            )

        print(
            f"[GIF] Loaded dinner.gif "
            f"({frame_count} frames)"
        )

    except Exception as error:

        print(
            "[GIF ERROR]"
        )

        print(error)


load_gif()


def update_gif(dt):

    global gif_index
    global gif_timer

    if not gif_frames:
        return

    gif_timer += dt

    if gif_timer >= gif_durations[
        gif_index
    ]:

        gif_timer = 0

        gif_index += 1

        if gif_index >= len(
            gif_frames
        ):

            gif_index = 0


def get_gif_frame():

    if not gif_frames:
        return None

    return gif_frames[
        gif_index
    ]


# ============================================================
# SCENE STATE
# ============================================================

scene = "menu"

menu_options = [
    "BREAKFAST",
    "LUNCH",
    "DINNER"
]

selected_option = 0

# Tracks the option currently under the mouse.
last_hovered_option = -1

transition_alpha = 0
transitioning = False
transition_target = None
transition_phase = "out"


# ============================================================
# TRANSITIONS
# ============================================================

def begin_transition(target):

    global transitioning
    global transition_target
    global transition_phase

    if transitioning:
        return

    transition_target = target
    transition_phase = "out"
    transitioning = True


def change_scene(target):

    global scene
    global selected_option
    global gif_index
    global gif_timer
    global last_hovered_option

    scene = target

    last_hovered_option = -1

    if scene == "menu":

        play_music(
            "menu"
        )

    elif scene == "breakfast":

        play_music(
            "breakfast"
        )

    elif scene == "lunch":

        play_music(
            "lunch"
        )

    elif scene == "dinner":

        gif_index = 0
        gif_timer = 0

        reset_love_you_shower()

        play_music(
            "dinner"
        )

    selected_option = 0


def update_transition(dt):

    global transition_alpha
    global transitioning
    global transition_phase

    if not transitioning:
        return

    speed = 500

    if transition_phase == "out":

        transition_alpha += (
            speed * dt / 1000
        )

        if transition_alpha >= 255:

            transition_alpha = 255

            change_scene(
                transition_target
            )

            transition_phase = "in"

    elif transition_phase == "in":

        transition_alpha -= (
            speed * dt / 1000
        )

        if transition_alpha <= 0:

            transition_alpha = 0
            transitioning = False


def draw_transition():

    if transition_alpha <= 0:
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    overlay.fill(
        BLACK
    )

    overlay.set_alpha(
        int(transition_alpha)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


# ============================================================
# DRAWING HELPERS
# ============================================================

def draw_centered_text(
    text,
    font,
    y,
    color=WHITE
):

    surface = font.render(
        text,
        True,
        color
    )

    x = (
        WIDTH -
        surface.get_width()
    ) // 2

    screen.blit(
        surface,
        (x, y)
    )


def draw_overlay(alpha=130):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, alpha)
    )

    screen.blit(
        overlay,
        (0, 0)
    )


# ============================================================
# GRADIENT TEXT
# ============================================================

def create_gradient_text(
    text,
    font,
    left_color,
    right_color
):

    mask = font.render(
        text,
        True,
        (255, 255, 255)
    )

    width = mask.get_width()
    height = mask.get_height()

    gradient = pygame.Surface(
        (width, height),
        pygame.SRCALPHA
    )

    for x in range(width):

        if width <= 1:

            ratio = 0

        else:

            ratio = x / (
                width - 1
            )

        r = int(
            left_color[0] +
            (
                right_color[0] -
                left_color[0]
            ) * ratio
        )

        g = int(
            left_color[1] +
            (
                right_color[1] -
                left_color[1]
            ) * ratio
        )

        b = int(
            left_color[2] +
            (
                right_color[2] -
                left_color[2]
            ) * ratio
        )

        pygame.draw.line(
            gradient,
            (r, g, b, 255),
            (x, 0),
            (x, height)
        )

    gradient.blit(
        mask,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    return gradient


# ============================================================
# GRADIENT BORDER
# ============================================================

def draw_gradient_border(
    rect,
    left_color,
    right_color,
    width=2
):

    # Top and bottom
    for x in range(
        rect.x,
        rect.x + rect.width
    ):

        ratio = (
            x - rect.x
        ) / max(
            1,
            rect.width - 1
        )

        color = tuple(
            int(
                left_color[i] +
                (
                    right_color[i] -
                    left_color[i]
                ) * ratio
            )
            for i in range(3)
        )

        pygame.draw.line(
            screen,
            color,
            (
                x,
                rect.y
            ),
            (
                x,
                rect.y + width - 1
            )
        )

        pygame.draw.line(
            screen,
            color,
            (
                x,
                rect.bottom - width
            ),
            (
                x,
                rect.bottom - 1
            )
        )

    # Left and right
    for y in range(
        rect.y,
        rect.y + rect.height
    ):

        ratio = (
            y - rect.y
        ) / max(
            1,
            rect.height - 1
        )

        color = tuple(
            int(
                left_color[i] +
                (
                    right_color[i] -
                    left_color[i]
                ) * ratio
            )
            for i in range(3)
        )

        pygame.draw.line(
            screen,
            color,
            (
                rect.x,
                y
            ),
            (
                rect.x + width - 1,
                y
            )
        )

        pygame.draw.line(
            screen,
            color,
            (
                rect.right - width,
                y
            ),
            (
                rect.right - 1,
                y
            )
        )


# ============================================================
# MAIN MENU PANEL
# ============================================================

MENU_PANEL_WIDTH = 560
MENU_PANEL_HEIGHT = 430

MENU_PANEL_X = (
    WIDTH -
    MENU_PANEL_WIDTH
) // 2

MENU_PANEL_Y = (
    HEIGHT -
    MENU_PANEL_HEIGHT
) // 2


def draw_menu_panel():

    x = MENU_PANEL_X
    y = MENU_PANEL_Y

    # --------------------------------------------------------
    # MAIN BLUE-BLACK PANEL
    # --------------------------------------------------------

    panel = pygame.Surface(
        (
            MENU_PANEL_WIDTH,
            MENU_PANEL_HEIGHT
        ),
        pygame.SRCALPHA
    )

    panel.fill(
        PANEL_BLUE
    )

    screen.blit(
        panel,
        (x, y)
    )

    # --------------------------------------------------------
    # OUTER BORDER
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        PANEL_BORDER,
        (
            x,
            y,
            MENU_PANEL_WIDTH,
            MENU_PANEL_HEIGHT
        ),
        2
    )

    # --------------------------------------------------------
    # INNER BORDER
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        PANEL_INNER,
        (
            x + 8,
            y + 8,
            MENU_PANEL_WIDTH - 16,
            MENU_PANEL_HEIGHT - 16
        ),
        1
    )


# ============================================================
# MENU OPTION RECTANGLES
# ============================================================

def get_menu_option_rects():

    rects = []

    start_y = (
        MENU_PANEL_Y + 165
    )

    spacing = 58

    for index in range(
        len(menu_options)
    ):

        text = MENU_FONT.render(
            menu_options[index],
            True,
            WHITE
        )

        rect = pygame.Rect(
            0,
            0,
            text.get_width() + 80,
            48
        )

        rect.centerx = (
            MENU_PANEL_X +
            MENU_PANEL_WIDTH // 2
        )

        rect.y = (
            start_y +
            index * spacing
        )

        rects.append(
            rect
        )

    return rects


# ============================================================
# PIXEL ARROW
# ============================================================

def draw_pixel_arrow(
    x,
    y,
    time_ms
):

    movement = int(
        math.sin(
            time_ms / 220
        ) * 3
    )

    x += movement

    blue_points = [
        (x + 2, y),
        (x + 17, y + 7),
        (x + 11, y + 7),
        (x + 11, y + 14),
        (x + 6, y + 14),
        (x + 6, y + 10),
        (x + 2, y + 10)
    ]

    pink_points = [
        (x, y),
        (x + 15, y + 7),
        (x + 9, y + 7),
        (x + 9, y + 14),
        (x + 4, y + 14),
        (x + 4, y + 10),
        (x, y + 10)
    ]

    pygame.draw.polygon(
        screen,
        ARROW_BLUE,
        blue_points
    )

    pygame.draw.polygon(
        screen,
        ARROW_PINK,
        pink_points
    )


# ============================================================
# MAIN MENU
# ============================================================

def draw_menu():

    global selected_option
    global last_hovered_option

    frame = get_video_frame()

    if frame is not None:

        screen.blit(
            frame,
            (0, 0)
        )

    else:

        screen.fill(
            DARK_BLUE
        )

    draw_overlay(
        90
    )

    draw_menu_panel()

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = create_gradient_text(
        "FROM ME TO YOU",
        TITLE_FONT,
        DARK_PINK,
        BLUE
    )

    title_x = (
        MENU_PANEL_X +
        (
            MENU_PANEL_WIDTH -
            title.get_width()
        ) // 2
    )

    title_y = (
        MENU_PANEL_Y +
        42
    )

    screen.blit(
        title,
        (
            title_x,
            title_y
        )
    )

    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    option_rects = (
        get_menu_option_rects()
    )

    mouse_pos = pygame.mouse.get_pos()

    if not transitioning:

        current_hovered_option = -1

        for index, rect in enumerate(
            option_rects
        ):

            if rect.collidepoint(
                mouse_pos
            ):

                current_hovered_option = index
                selected_option = index

                break

        # Play hover sound only when entering
        # a new menu option.
        if (
            current_hovered_option !=
            last_hovered_option
        ):

            if current_hovered_option != -1:

                play_hover_sound()

            last_hovered_option = (
                current_hovered_option
            )

    for index, option in enumerate(
        menu_options
    ):

        rect = option_rects[
            index
        ]

        is_selected = (
            index ==
            selected_option
        )

        if is_selected:

            text_color = (
                MENU_SELECTED
            )

            selection_box = pygame.Rect(
                rect.x + 20,
                rect.y,
                rect.width - 40,
                rect.height
            )

            pygame.draw.rect(
                screen,
                (22, 28, 45),
                selection_box
            )

            pygame.draw.rect(
                screen,
                (58, 48, 67),
                selection_box,
                1
            )

            text = MENU_FONT.render(
                option,
                True,
                text_color
            )

            text_x = (
                rect.centerx -
                text.get_width() // 2
            )

            text_y = (
                rect.centery -
                text.get_height() // 2
            )

            arrow_x = (
                text_x -
                28
            )

            arrow_y = (
                text_y +
                5
            )

            draw_pixel_arrow(
                arrow_x,
                arrow_y,
                pygame.time.get_ticks()
            )

        else:

            text_color = MENU_RED

            text = MENU_FONT.render(
                option,
                True,
                text_color
            )

            text_x = (
                rect.centerx -
                text.get_width() // 2
            )

            text_y = (
                rect.centery -
                text.get_height() // 2
            )

        screen.blit(
            text,
            (
                text_x,
                text_y
            )
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    footer = SMALL_FONT.render(
        "Go ahead... choose.",
        True,
        WHITE
    )

    footer_x = (
        MENU_PANEL_X +
        (
            MENU_PANEL_WIDTH -
            footer.get_width()
        ) // 2
    )

    footer_y = (
        MENU_PANEL_Y +
        MENU_PANEL_HEIGHT -
        52
    )

    screen.blit(
        footer,
        (
            footer_x,
            footer_y
        )
    )


# ============================================================
# MENU SELECTION
# ============================================================

def choose_menu_option():

    # Play click sound when selecting.
    play_click_sound()

    if selected_option == 0:

        begin_transition(
            "breakfast"
        )

    elif selected_option == 1:

        begin_transition(
            "lunch"
        )

    elif selected_option == 2:

        begin_transition(
            "dinner"
        )


# ============================================================
# MEAL SCENES
# ============================================================

def draw_meal_scene(
    background,
    title,
    description
):

    if background is not None:

        screen.blit(
            background,
            (0, 0)
        )

    else:

        screen.fill(
            DARK_BLUE
        )

    draw_overlay(
        75
    )

    # --------------------------------------------------------
    # TOP TITLE PANEL
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        (10, 15, 25, 170),
        (
            40,
            35,
            1120,
            105
        )
    )

    title_surface = create_gradient_text(
        title,
        TITLE_FONT,
        MEAL_RED,
        MEAL_BLUE
    )

    screen.blit(
        title_surface,
        (
            70,
            48
        )
    )

    # --------------------------------------------------------
    # DESCRIPTION PANEL
    # --------------------------------------------------------

    panel_rect = pygame.Rect(
        70,
        490,
        WIDTH - 140,
        150
    )

    panel = pygame.Surface(
        (
            panel_rect.width,
            panel_rect.height
        ),
        pygame.SRCALPHA
    )

    panel.fill(
        (8, 12, 22, 125)
    )

    screen.blit(
        panel,
        panel_rect.topleft
    )

    # Blue-red border.
    draw_gradient_border(
        panel_rect,
        BORDER_BLUE,
        BORDER_RED,
        2
    )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    description_surface = create_gradient_text(
        description,
        BODY_FONT,
        DESCRIPTION_PINK,
        DESCRIPTION_BLUE
    )

    description_x = (
        WIDTH -
        description_surface.get_width()
    ) // 2

    screen.blit(
        description_surface,
        (
            description_x,
            525
        )
    )

    # --------------------------------------------------------
    # ESC INSTRUCTION
    # --------------------------------------------------------

    esc_surface = ESC_FONT.render(
        "ESC  TO RETURN TO MAIN MENU",
        True,
        BLACK
    )

    esc_x = (
        WIDTH -
        esc_surface.get_width() -
        30
    )

    esc_y = (
        HEIGHT -
        esc_surface.get_height() -
        22
    )

    screen.blit(
        esc_surface,
        (
            esc_x,
            esc_y
        )
    )


def draw_breakfast():

    draw_meal_scene(
        breakfast_background,
        "BREAKFAST",
        "Pancakes and Mountain Dew sound like a great combo... maybe sprinkle some chicken wings."
    )


def draw_lunch():

    draw_meal_scene(
        lunch_background,
        "LUNCH",
        "Chicken rice with sweet and sour chicken with braised pork ribs.... oooo and iced teaa"
    )


# ============================================================
# DINNER — I LOVE YOU SHOWER
# ============================================================

love_you_active = False
love_you_timer = 0

love_you_particles = []


def make_heart_surface(size=18):

    surface = pygame.Surface(
        (
            size * 2,
            size * 2
        ),
        pygame.SRCALPHA
    )

    pink = (
        210,
        65,
        125,
        235
    )

    pygame.draw.circle(
        surface,
        pink,
        (
            size // 2,
            size // 2
        ),
        size // 2
    )

    pygame.draw.circle(
        surface,
        pink,
        (
            size + size // 2,
            size // 2
        ),
        size // 2
    )

    pygame.draw.polygon(
        surface,
        pink,
        [
            (
                1,
                size // 2
            ),
            (
                size * 2 - 1,
                size // 2
            ),
            (
                size,
                size * 2
            )
        ]
    )

    return surface


def create_love_particle():

    particle_type = random.choice(
        [
            "text",
            "heart"
        ]
    )

    x = random.randint(
        0,
        WIDTH
    )

    y = random.randint(
        -HEIGHT,
        -30
    )

    speed = random.uniform(
        45,
        115
    )

    drift = random.uniform(
        -22,
        22
    )

    if particle_type == "text":

        font_size = random.randint(
            18,
            29
        )

        font = pygame.font.SysFont(
            "segoeui",
            font_size,
            bold=True
        )

        color_start = random.choice(
            [
                DINNER_BLUE,
                DINNER_PINK
            ]
        )

        color_end = random.choice(
            [
                DINNER_PINK,
                DINNER_BLUE
            ]
        )

        surface = create_gradient_text(
            "I LOVE YOU",
            font,
            color_start,
            color_end
        )

    else:

        size = random.randint(
            9,
            15
        )

        surface = make_heart_surface(
            size
        )

    return {
        "type": particle_type,
        "x": float(x),
        "y": float(y),
        "speed": speed,
        "drift": drift,
        "surface": surface,
        "phase": random.uniform(
            0,
            math.pi * 2
        )
    }


def reset_love_you_shower():

    global love_you_particles
    global love_you_active

    love_you_particles = []
    love_you_active = False


def trigger_love_you():

    global love_you_active
    global love_you_timer
    global love_you_particles

    love_you_active = True
    love_you_timer = 0

    love_you_particles = []

    # Lots of smaller words and hearts.
    for _ in range(45):

        love_you_particles.append(
            create_love_particle()
        )


def update_love_you(dt):

    global love_you_timer
    global love_you_particles

    if not love_you_active:
        return

    love_you_timer += dt

    seconds = dt / 1000

    for particle in love_you_particles:

        particle["y"] += (
            particle["speed"] *
            seconds
        )

        particle["x"] += (
            particle["drift"] *
            seconds
        )

        particle["phase"] += (
            seconds * 2
        )

        particle["x"] += (
            math.sin(
                particle["phase"]
            ) * 0.4
        )

        if particle["y"] > HEIGHT + 50:

            particle["y"] = random.randint(
                -120,
                -20
            )

            particle["x"] = random.randint(
                0,
                WIDTH
            )


def draw_love_you_shower():

    if not love_you_active:
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 35)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    for particle in love_you_particles:

        surface = particle["surface"]

        x = int(
            particle["x"]
        )

        y = int(
            particle["y"]
        )

        shadow = surface.copy()

        shadow.set_alpha(
            100
        )

        screen.blit(
            shadow,
            (
                x + 2,
                y + 2
            )
        )

        screen.blit(
            surface,
            (
                x,
                y
            )
        )


def draw_dinner():

    frame = get_gif_frame()

    if frame is not None:

        screen.blit(
            frame,
            (0, 0)
        )

    else:

        screen.fill(
            (20, 10, 20)
        )

    draw_overlay(
        55
    )

    # --------------------------------------------------------
    # DINNER TITLE
    # --------------------------------------------------------

    title = create_gradient_text(
        "DINNER",
        SMALL_FONT,
        DINNER_BLUE,
        DINNER_PINK
    )

    screen.blit(
        title,
        (
            40,
            30
        )
    )

    # --------------------------------------------------------
    # CLICK ANYWHERE
    # --------------------------------------------------------

    instruction = SMALL_FONT.render(
        "CLICK ANYWHERE",
        True,
        BLACK
    )

    screen.blit(
        instruction,
        (
            WIDTH -
            instruction.get_width() -
            40,
            30
        )
    )

    # --------------------------------------------------------
    # MIDDLE MESSAGE
    # --------------------------------------------------------

    if love_you_active:

        draw_love_you_shower()

    else:

        draw_centered_text(
            "and one last thing...",
            SMALL_FONT,
            HEIGHT // 2 - 20,
            WHITE
        )

    # --------------------------------------------------------
    # ESC — BOTTOM RIGHT
    # --------------------------------------------------------

    esc_surface = ESC_FONT.render(
        "ESC  TO RETURN TO MAIN MENU",
        True,
        BLACK
    )

    esc_x = (
        WIDTH -
        esc_surface.get_width() -
        30
    )

    esc_y = (
        HEIGHT -
        esc_surface.get_height() -
        22
    )

    screen.blit(
        esc_surface,
        (
            esc_x,
            esc_y
        )
    )


# ============================================================
# MAIN LOOP
# ============================================================

running = True

play_music(
    "menu"
)

print()
print(
    "======================================"
)

print(
    "          FROM ME TO YOU"
)

print(
    "======================================"
)

print()

print(
    "Controls:"
)

print(
    "UP / DOWN  - Select"
)

print(
    "ENTER      - Choose"
)

print(
    "ESC        - Return to menu"
)

print(
    "CLICK      - Select / trigger dinner"
)

print()

print(
    "Music starts at 45 seconds."
)

print()

print(
    "Game starting..."
)

print()


while running:

    dt = clock.tick(
        FPS
    )

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # ----------------------------------------------------
        # KEYBOARD
        # ----------------------------------------------------

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if scene != "menu":

                    begin_transition(
                        "menu"
                    )

            elif scene == "menu":

                if event.key == pygame.K_UP:

                    selected_option -= 1

                    if selected_option < 0:

                        selected_option = (
                            len(menu_options) - 1
                        )

                    play_hover_sound()

                elif event.key == pygame.K_DOWN:

                    selected_option += 1

                    if selected_option >= len(
                        menu_options
                    ):

                        selected_option = 0

                    play_hover_sound()

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    choose_menu_option()

        # ----------------------------------------------------
        # MOUSE
        # ----------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            if scene == "menu":

                option_rects = (
                    get_menu_option_rects()
                )

                for index, rect in enumerate(
                    option_rects
                ):

                    if rect.collidepoint(
                        mouse_x,
                        mouse_y
                    ):

                        selected_option = index

                        choose_menu_option()

                        break

            elif scene == "dinner":

                trigger_love_you()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    if scene == "dinner":

        update_gif(
            dt
        )

        update_love_you(
            dt
        )

    update_transition(
        dt
    )

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    if scene == "menu":

        draw_menu()

    elif scene == "breakfast":

        draw_breakfast()

    elif scene == "lunch":

        draw_lunch()

    elif scene == "dinner":

        draw_dinner()

    draw_transition()

    pygame.display.flip()


# ============================================================
# CLEANUP
# ============================================================

pygame.mixer.music.stop()

if video is not None:

    video.release()

pygame.quit()

sys.exit()