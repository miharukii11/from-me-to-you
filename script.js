```javascript
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

const backgroundVideo =
    document.getElementById("background-video");

const startScreen =
    document.getElementById("start-screen");

const transition =
    document.getElementById("transition");

const menuScene =
    document.getElementById("menu-scene");

const breakfastScene =
    document.getElementById("breakfast-scene");

const lunchScene =
    document.getElementById("lunch-scene");

const dinnerScene =
    document.getElementById("dinner-scene");

const menuOptions =
    Array.from(document.querySelectorAll(".menu-option"));

const returnButtons =
    Array.from(document.querySelectorAll(".return-button"));

const dinnerSceneElement =
    document.getElementById("dinner-scene");

const dinnerMessage =
    document.getElementById("dinner-message");

const loveShower =
    document.getElementById("love-shower");


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


const breakfastSceneImage =
    document.createElement("img");

const lunchSceneImage =
    document.createElement("img");


breakfastSceneImage.className =
    "meal-background-image";

lunchSceneImage.className =
    "meal-background-image";


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
        breakfastImageCandidates[
            breakfastImageIndex
        ];

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
        lunchImageCandidates[
            lunchImageIndex
        ];

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

const mealBackgroundStyle = document.createElement("style");

mealBackgroundStyle.textContent = `
    .meal-background-image {
        position: absolute;
        inset: 0;

        width: 100%;
        height: 100%;

        object-fit: cover;

        z-index: 0;
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

        audio.pause();

        try {
            audio.currentTime = 0;
        } catch (error) {
            // Ignore browsers that do not allow this yet.
        }
    });
}


function playMusic(audio) {

    stopAllMusic();

    if (!audio) {
        return;
    }

    /*
       The browser needs the audio metadata before
       currentTime can reliably be set.
    */

    const startAudio = () => {

        try {
            audio.currentTime =
                MUSIC_START_SECONDS;
        } catch (error) {
            // Continue anyway.
        }

        const playPromise =
            audio.play();

        if (
            playPromise &&
            typeof playPromise.catch === "function"
        ) {
            playPromise.catch(() => {
                /*
                   Mobile browsers may block audio until
                   the user taps the page. The first
                   interaction will try again.
                */
            });
        }
    };


    if (audio.readyState >= 1) {

        startAudio();

    } else {

        audio.addEventListener(
            "loadedmetadata",
            startAudio,
            { once: true }
        );

        audio.load();
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

    if (!audioStarted) {
        return;
    }

    try {

        hoverSound.currentTime = 0;

        const promise =
            hoverSound.play();

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

    if (!audioStarted) {
        return;
    }

    try {

        clickSound.currentTime = 0;

        const promise =
            clickSound.play();

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

function beginGame() {

    startAudio();

    startScreen.classList.add("hidden");
}


startScreen.addEventListener(
    "click",
    beginGame
);

startScreen.addEventListener(
    "touchstart",
    beginGame,
    { passive: true }
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

        /*
           Main menu controls
        */

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


        /*
           ESC returns to the menu
        */

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
   TOUCH / MOBILE KEYBOARD SUPPORT
   ========================================================= */

document.addEventListener(
    "touchstart",
    () => {

        startAudio();

    },
    {
        passive: true,
        once: true
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

        dinnerMessage.style.display =
            "block";

        loveShower.innerHTML = "";
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


    transition.classList.add(
        "active"
    );


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


            setMusicForScene(
                sceneName
            );


            setTimeout(
                () => {

                    transition.classList.remove(
                        "active"
                    );

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


    dinnerMessage.style.display =
        "none";


    loveShower.innerHTML = "";


    createLoveParticles();
}


/* =========================================================
   CREATE LOVE PARTICLES
   ========================================================= */

function createLoveParticles() {

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


        /*
           Slightly different sizes so the
           shower does not look too uniform.
        */

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

dinnerSceneElement.addEventListener(
    "click",
    (event) => {

        /*
           Don't activate the shower if the user
           clicked the return button.
        */

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


/* =========================================================
   PREVENT DOUBLE-TAP ZOOM ON MOBILE
   ========================================================= */

let lastTouchTime = 0;

document.addEventListener(
    "touchend",
    (event) => {

        const now =
            Date.now();

        if (
            now - lastTouchTime <= 300
        ) {

            event.preventDefault();
        }

        lastTouchTime = now;
    },
    {
        passive: false
    }
);


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
            /*
               Some browsers require user interaction
               before video playback.
            */
        });
    }
}


startBackgroundVideo();


/* =========================================================
   INITIAL STATE
   ========================================================= */

updateMenuSelection(
    0,
    false
);


/*
   Keep the menu music stopped until the user
   interacts with the start screen.

   This is necessary because phones commonly
   block automatic audio playback.
*/

stopAllMusic();
```
