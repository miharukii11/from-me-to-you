/* =========================================================
   FROM ME TO YOU
   Game logic
   ========================================================= */

"use strict";

/* =========================================================
   SETTINGS
   ========================================================= */

const MUSIC_START_SECONDS = 45;
const TRANSITION_TIME = 350;
const LOVE_PARTICLE_COUNT = 45;


/* =========================================================
   ELEMENTS
   ========================================================= */

const backgroundVideo = document.getElementById("background-video");

const startScreen = document.getElementById("start-screen");
const transition = document.getElementById("transition");

const menuScene = document.getElementById("menu-scene");
const breakfastScene = document.getElementById("breakfast-scene");
const lunchScene = document.getElementById("lunch-scene");
const dinnerScene = document.getElementById("dinner-scene");

const menuOptions =
    Array.from(document.querySelectorAll(".menu-option"));

const returnButtons =
    Array.from(document.querySelectorAll(".return-button"));

const dinnerMessage =
    document.getElementById("dinner-message");

const loveShower =
    document.getElementById("love-shower");

const dinnerBackground =
    document.getElementById("dinner-background");


/* =========================================================
   AUDIO
   ========================================================= */

const menuMusic =
    document.getElementById("menu-music");

const breakfastMusic =
    document.getElementById("breakfast-music");

const lunchMusic =
    document.getElementById("lunch-music");

const dinnerMusic =
    document.getElementById("dinner-music");

const hoverSound =
    document.getElementById("hover-sound");

const clickSound =
    document.getElementById("click-sound");


const allMusic = [
    menuMusic,
    breakfastMusic,
    lunchMusic,
    dinnerMusic
];


/* =========================================================
   GAME STATE
   ========================================================= */

let currentScene = "menu";
let selectedIndex = 0;
let dinnerActivated = false;
let audioStarted = false;


/* =========================================================
   BACKGROUND IMAGE SUPPORT
   ========================================================= */

const breakfastImageCandidates = [
    "images/breakfast.png",
    "images/breakfast.jpg",
    "images/breakfast.jpeg",
    "images/breakfast.webp"
];

const lunchImageCandidates = [
    "images/lunch.png",
    "images/lunch.jpg",
    "images/lunch.jpeg",
    "images/lunch.webp"
];

let breakfastImageIndex = 0;
let lunchImageIndex = 0;

const breakfastSceneImage = document.createElement("img");
const lunchSceneImage = document.createElement("img");

breakfastSceneImage.className = "meal-background-image";
lunchSceneImage.className = "meal-background-image";

breakfastSceneImage.alt = "";
lunchSceneImage.alt = "";

breakfastScene.insertBefore(
    breakfastSceneImage,
    breakfastScene.firstChild
);

lunchScene.insertBefore(
    lunchSceneImage,
    lunchScene.firstChild
);


/* =========================================================
   FIND BREAKFAST IMAGE
   ========================================================= */

function loadBreakfastImage() {

    if (
        breakfastImageIndex >=
        breakfastImageCandidates.length
    ) {
        return;
    }

    const candidate =
        breakfastImageCandidates[breakfastImageIndex];

    breakfastSceneImage.src = candidate;

    breakfastSceneImage.onerror = () => {

        breakfastImageIndex++;

        loadBreakfastImage();
    };
}


/* =========================================================
   FIND LUNCH IMAGE
   ========================================================= */

function loadLunchImage() {

    if (
        lunchImageIndex >=
        lunchImageCandidates.length
    ) {
        return;
    }

    const candidate =
        lunchImageCandidates[lunchImageIndex];

    lunchSceneImage.src = candidate;

    lunchSceneImage.onerror = () => {

        lunchImageIndex++;

        loadLunchImage();
    };
}


loadBreakfastImage();
loadLunchImage();


/* =========================================================
   MEAL BACKGROUND STYLING
   ========================================================= */

const mealBackgroundStyle =
    document.createElement("style");

mealBackgroundStyle.textContent = `
    .meal-background-image {
        position: absolute;
        inset: 0;

        width: 100%;
        height: 100%;

        object-fit: cover;

        z-index: 0;
        pointer-events: none;
    }

    .meal-scene::after {
        content: "";

        position: absolute;
        inset: 0;

        background: rgba(4, 7, 15, 0.16);

        z-index: 1;

        pointer-events: none;
    }

    .meal-scene .meal-title-panel,
    .meal-scene .description-panel,
    .meal-scene .return-button {
        z-index: 5;
    }
`;

document.head.appendChild(mealBackgroundStyle);


/* =========================================================
   AUDIO HELPERS
   ========================================================= */

function stopAllMusic() {

    allMusic.forEach((audio) => {

        if (!audio) {
            return;
        }

        audio.pause();

        try {
            audio.currentTime = 0;
        } catch (error) {
            // Ignore browser restrictions.
        }
    });
}


function playMusic(audio) {

    stopAllMusic();

    if (!audio) {
        return;
    }

    /*
       play() must be called right away, while the browser
       still counts this as part of the user's tap. Phones
       (especially iPhones) block sound that starts later.
       The jump to MUSIC_START_SECONDS happens as soon as
       the song's length is known.
    */

    const seekToStart = () => {
        try {
            audio.currentTime =
                MUSIC_START_SECONDS;
        } catch (error) {
            // Continue anyway.
        }
    };

    if (audio.readyState >= 1) {
        seekToStart();
    } else {
        audio.addEventListener(
            "loadedmetadata",
            seekToStart,
            { once: true }
        );
    }

    const playPromise = audio.play();

    if (
        playPromise &&
        typeof playPromise.catch === "function"
    ) {
        playPromise.catch(() => {
            // Browser may block audio.
        });
    }
}


/* =========================================================
   START AUDIO
   ========================================================= */

function startAudio() {

    if (audioStarted) {
        return;
    }

    audioStarted = true;

    playMusic(menuMusic);
}


/* =========================================================
   SOUND EFFECTS
   ========================================================= */

function playHoverSound() {

    if (!audioStarted || !hoverSound) {
        return;
    }

    try {

        hoverSound.currentTime = 0;

        const promise = hoverSound.play();

        if (
            promise &&
            typeof promise.catch === "function"
        ) {
            promise.catch(() => {});
        }

    } catch (error) {
        // Ignore sound errors.
    }
}


function playClickSound() {

    if (!audioStarted || !clickSound) {
        return;
    }

    try {

        clickSound.currentTime = 0;

        const promise = clickSound.play();

        if (
            promise &&
            typeof promise.catch === "function"
        ) {
            promise.catch(() => {});
        }

    } catch (error) {
        // Ignore sound errors.
    }
}


/* =========================================================
   START SCREEN
   ========================================================= */

function beginGame(event) {
    startAudio();

    if (startScreen) {
        startScreen.classList.add("hidden");
        // Force hide so it cannot obstruct clicks underneath
        setTimeout(() => {
            startScreen.style.display = "none";
        }, 450);
    }
}


/*
   The start screen itself.
*/

if (startScreen) {

    startScreen.addEventListener(
        "click",
        beginGame
    );
}


/*
   Keyboard users can also start the game.
*/

document.addEventListener(
    "keydown",
    () => {

        if (!audioStarted) {
            startAudio();

            if (startScreen) {
                startScreen.classList.add("hidden");
                startScreen.style.pointerEvents = "none";

                setTimeout(() => {
                    startScreen.style.display = "none";
                }, 450);
            }
        }

    },
    {
        once: true
    }
);


/* =========================================================
   MENU SELECTION
   ========================================================= */

function updateMenuSelection(
    newIndex,
    playSound = true
) {

    if (menuOptions.length === 0) {
        return;
    }

    newIndex =
        (newIndex + menuOptions.length) %
        menuOptions.length;


    if (
        playSound &&
        newIndex !== selectedIndex
    ) {

        playHoverSound();
    }


    selectedIndex = newIndex;


    menuOptions.forEach(
        (option, index) => {

            option.classList.toggle(
                "selected",
                index === selectedIndex
            );

        }
    );
}


/* =========================================================
   MENU MOUSE / TOUCH
   ========================================================= */

menuOptions.forEach(
    (option, index) => {

        option.addEventListener(
            "mouseenter",
            () => {

                if (
                    currentScene !== "menu"
                ) {
                    return;
                }

                updateMenuSelection(index);
            }
        );


        option.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                if (
                    currentScene !== "menu"
                ) {
                    return;
                }

                updateMenuSelection(
                    index,
                    false
                );

                playClickSound();

                const scene =
                    option.dataset.scene;

                openScene(scene);
            }
        );

    }
);


/* =========================================================
   KEYBOARD CONTROLS
   ========================================================= */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            currentScene === "menu"
        ) {

            if (
                event.key === "ArrowUp" ||
                event.key === "w" ||
                event.key === "W"
            ) {

                event.preventDefault();

                updateMenuSelection(
                    selectedIndex - 1
                );

                return;
            }


            if (
                event.key === "ArrowDown" ||
                event.key === "s" ||
                event.key === "S"
            ) {

                event.preventDefault();

                updateMenuSelection(
                    selectedIndex + 1
                );

                return;
            }


            if (
                event.key === "Enter" ||
                event.key === " "
            ) {

                event.preventDefault();

                playClickSound();

                const selectedOption =
                    menuOptions[selectedIndex];

                if (selectedOption) {

                    openScene(
                        selectedOption.dataset.scene
                    );
                }

                return;
            }
        }


        if (
            event.key === "Escape"
        ) {

            event.preventDefault();

            if (
                currentScene !== "menu"
            ) {

                openScene("menu");
            }
        }

    }
);


/* =========================================================
   SCENE MANAGEMENT
   ========================================================= */

function getSceneElement(sceneName) {

    switch (sceneName) {

        case "menu":
            return menuScene;

        case "breakfast":
            return breakfastScene;

        case "lunch":
            return lunchScene;

        case "dinner":
            return dinnerScene;

        default:
            return menuScene;
    }
}


function prepareScene(sceneName) {

    if (
        sceneName === "dinner"
    ) {

        dinnerActivated = false;

        if (dinnerMessage) {
            dinnerMessage.style.display = "block";
        }

        if (loveShower) {
            loveShower.innerHTML = "";
        }

        playDinnerBackground();

    } else if (dinnerBackground) {

        dinnerBackground.pause();
    }
}


function playDinnerBackground() {

    if (
        !dinnerBackground ||
        typeof dinnerBackground.play !== "function"
    ) {
        return;
    }

    dinnerBackground.muted = true;
    dinnerBackground.playsInline = true;

    const promise = dinnerBackground.play();

    if (
        promise &&
        typeof promise.catch === "function"
    ) {
        promise.catch(() => {});
    }
}


function setMusicForScene(sceneName) {

    switch (sceneName) {

        case "menu":
            playMusic(menuMusic);
            break;

        case "breakfast":
            playMusic(breakfastMusic);
            break;

        case "lunch":
            playMusic(lunchMusic);
            break;

        case "dinner":
            playMusic(dinnerMusic);
            break;

        default:
            playMusic(menuMusic);
    }
}


/* =========================================================
   OPEN SCENE
   ========================================================= */

function openScene(sceneName) {

    if (
        sceneName === currentScene
    ) {
        return;
    }


    const nextScene =
        getSceneElement(sceneName);


    if (!nextScene) {
        return;
    }


    // Start the new song now, while still inside the tap.
    setMusicForScene(sceneName);


    if (transition) {
        transition.classList.add("active");
    }


    setTimeout(
        () => {

            document
                .querySelectorAll(".scene")
                .forEach(
                    (scene) => {

                        scene.classList.remove(
                            "active"
                        );

                    }
                );


            prepareScene(sceneName);


            nextScene.classList.add(
                "active"
            );


            currentScene =
                sceneName;


            if (
                sceneName === "menu"
            ) {

                updateMenuSelection(
                    selectedIndex,
                    false
                );
            }


            setTimeout(
                () => {

                    if (transition) {
                        transition.classList.remove(
                            "active"
                        );
                    }

                },
                40
            );

        },
        TRANSITION_TIME
    );
}


/* =========================================================
   RETURN BUTTONS
   ========================================================= */

returnButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                playClickSound();

                openScene("menu");
            }
        );

    }
);


/* =========================================================
   DINNER LOVE SHOWER
   ========================================================= */

function activateDinner() {

    if (
        currentScene !== "dinner"
    ) {
        return;
    }


    if (dinnerActivated) {
        return;
    }


    dinnerActivated = true;


    if (dinnerMessage) {
        dinnerMessage.style.display = "none";
    }


    if (loveShower) {
        loveShower.innerHTML = "";
    }


    createLoveParticles();
}


/* =========================================================
   CREATE LOVE PARTICLES
   ========================================================= */

function createLoveParticles() {

    if (!loveShower) {
        return;
    }

    for (
        let i = 0;
        i < LOVE_PARTICLE_COUNT;
        i++
    ) {

        const particle =
            document.createElement("div");


        const useHeart =
            Math.random() < 0.35;


        particle.className =
            useHeart
                ? "love-heart"
                : "love-particle";


        particle.textContent =
            useHeart
                ? "♥"
                : "I LOVE YOU";


        const left =
            Math.random() * 100;


        const duration =
            4 +
            Math.random() * 5;


        const delay =
            Math.random() * 5;


        const drift =
            -100 +
            Math.random() * 200;


        particle.style.left =
            `${left}%`;


        particle.style.animationDuration =
            `${duration}s`;


        particle.style.animationDelay =
            `${delay}s`;


        particle.style.setProperty(
            "--drift",
            `${drift}px`
        );


        if (!useHeart) {

            const size =
                13 +
                Math.random() * 8;

            particle.style.fontSize =
                `${size}px`;
        }


        loveShower.appendChild(
            particle
        );
    }
}


/* =========================================================
   DINNER CLICK
   ========================================================= */

if (dinnerScene) {

    dinnerScene.addEventListener(
        "click",
        (event) => {

            if (
                event.target.closest(
                    ".return-button"
                )
            ) {
                return;
            }


            playClickSound();

            activateDinner();
        }
    );
}


/*
   Double-tap zoom is turned off in style.css with
   "touch-action: manipulation", so quick taps are
   never swallowed.
*/


/* =========================================================
   VIDEO
   ========================================================= */

function startBackgroundVideo() {

    if (!backgroundVideo) {
        return;
    }


    backgroundVideo.muted = true;

    backgroundVideo.playsInline = true;


    const promise =
        backgroundVideo.play();


    if (
        promise &&
        typeof promise.catch === "function"
    ) {

        promise.catch(() => {
            // User interaction may be required.
        });
    }
}


startBackgroundVideo();


/*
   iPhones in Low Power Mode block autoplay.
   Try again on the first tap.
*/

document.addEventListener(
    "click",
    () => {
        if (backgroundVideo && backgroundVideo.paused) {
            startBackgroundVideo();
        }
    },
    { once: true }
);


/* =========================================================
   INITIAL STATE
   ========================================================= */

updateMenuSelection(
    0,
    false
);


/*
   Keep music stopped until the user interacts.
*/

stopAllMusic();
