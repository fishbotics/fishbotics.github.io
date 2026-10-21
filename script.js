/** Implementation of the presentation of the audio player */
import lottieWeb from 'https://cdn.skypack.dev/lottie-web';
import { LoopingAudio } from './looping-audio.js';

const playIconContainer = document.getElementById('play-icon');
const audioPlayerContainer = document.getElementById('audio-player');
const seekSlider = document.getElementById('seek-slider');
const volumeSlider = document.getElementById('volume-slider');
const muteIconContainer = document.getElementById('mute-icon');
let playState = 'play';
let muteState = 'unmute';

const playAnimation = lottieWeb.loadAnimation({
  container: playIconContainer,
  path: 'https://maxst.icons8.com/vue-static/landings/animated-icons/icons/pause/pause.json',
  renderer: 'svg',
  loop: false,
  autoplay: false,
  name: "Play Animation",
});

const muteAnimation = lottieWeb.loadAnimation({
    container: muteIconContainer,
    path: 'https://maxst.icons8.com/vue-static/landings/animated-icons/icons/mute/mute.json',
    renderer: 'svg',
    loop: false,
    autoplay: false,
    name: "Mute Animation",
});

playAnimation.goToAndStop(14, true);

playIconContainer.addEventListener('click', async () => {
    if(playState === 'play') {
        playIconContainer.disabled = true;
        try {
            await audio.play();
            playAnimation.playSegments([14, 27], true);
            raf = requestAnimationFrame(whilePlaying);
            playState = 'pause';
            playIconContainer.title = 'Pause';
        } catch (error) {
            console.error('Unable to play audio', error);
            playIconContainer.title = 'Unable to load audio. Click to retry.';
        } finally {
            playIconContainer.disabled = false;
        }
    } else {
        audio.pause();
        playAnimation.playSegments([0, 14], true);
        cancelAnimationFrame(raf);
        playState = 'play';
        playIconContainer.title = 'Play';
    }
});

muteIconContainer.addEventListener('click', () => {
    if(muteState === 'unmute') {
        muteAnimation.playSegments([0, 15], true);
        audio.muted = true;
        muteState = 'mute';
    } else {
        muteAnimation.playSegments([15, 25], true);
        audio.muted = false;
        muteState = 'unmute';
    }
    audio.updateVolume();
});

const showRangeProgress = (rangeInput) => {
    if(rangeInput === seekSlider) audioPlayerContainer.style.setProperty('--seek-before-width', rangeInput.value / rangeInput.max * 100 + '%');
    else audioPlayerContainer.style.setProperty('--volume-before-width', rangeInput.value / rangeInput.max * 100 + '%');
}

seekSlider.addEventListener('input', (e) => {
    showRangeProgress(e.target);
});
volumeSlider.addEventListener('input', (e) => {
    showRangeProgress(e.target);
});





/** Implementation of the functionality of the audio player */

const media = document.querySelector('audio');
const audio = new LoopingAudio(media.src, () => {
    displayDuration();
    setSliderMax();
    audioPlayerContainer.style.setProperty('--buffered-width', '100%');
});
const durationContainer = document.getElementById('duration');
const currentTimeContainer = document.getElementById('current-time');
const outputContainer = document.getElementById('volume-output');
let raf = null;

const calculateTime = (secs) => {
    const minutes = Math.floor(secs / 60);
    const seconds = Math.floor(secs % 60);
    const returnedSeconds = seconds < 10 ? `0${seconds}` : `${seconds}`;
    return `${minutes}:${returnedSeconds}`;
}

const displayDuration = () => {
    durationContainer.textContent = calculateTime(audio.duration || media.duration);
}

const setSliderMax = () => {
    seekSlider.max = audio.duration || media.duration;
    seekSlider.disabled = !audio.duration;
}

const displayBufferedAmount = () => {
    if (audio.duration || !media.buffered.length) return;
    const bufferedAmount = media.buffered.end(media.buffered.length - 1);
    audioPlayerContainer.style.setProperty('--buffered-width', `${(bufferedAmount / seekSlider.max) * 100}%`);
}

const whilePlaying = () => {
    seekSlider.value = Math.floor(audio.currentTime);
    currentTimeContainer.textContent = calculateTime(seekSlider.value);
    audioPlayerContainer.style.setProperty('--seek-before-width', `${seekSlider.value / seekSlider.max * 100}%`);
    raf = requestAnimationFrame(whilePlaying);
}

seekSlider.disabled = true;
if (media.readyState > 0) {
    displayDuration();
    setSliderMax();
    displayBufferedAmount();
} else {
    media.addEventListener('loadedmetadata', () => {
        displayDuration();
        setSliderMax();
        displayBufferedAmount();
    });
}

media.addEventListener('progress', displayBufferedAmount);

seekSlider.addEventListener('input', () => {
    currentTimeContainer.textContent = calculateTime(seekSlider.value);
    if(!audio.paused) {
        cancelAnimationFrame(raf);
    }
});

seekSlider.addEventListener('change', () => {
    audio.currentTime = seekSlider.value;
    if(!audio.paused) {
        raf = requestAnimationFrame(whilePlaying);
    }
});

volumeSlider.addEventListener('input', (e) => {
    const value = e.target.value;

    outputContainer.textContent = value;
    audio.volume = value / 100;
    audio.updateVolume();
});
