// The theme is 32 beats at 107 BPM. Keep its full duration: overlapping
// the ends would shorten the bar and make each repeat arrive early.
// Correct only the small waveform discontinuity at the wrap, tapering the
// correction to zero over 5 ms on either side without fading the music out.
export function smoothLoopBoundary(buffer) {
    const frames = Math.min(Math.round(buffer.sampleRate * 0.005), Math.floor(buffer.length / 2));
    if (frames < 2) return buffer;

    for (let channel = 0; channel < buffer.numberOfChannels; channel++) {
        const samples = buffer.getChannelData(channel);
        const last = samples.length - 1;
        const midpoint = (samples[0] + samples[last]) / 2;
        const startCorrection = midpoint - samples[0];
        const endCorrection = midpoint - samples[last];
        for (let i = 0; i < frames; i++) {
            const weight = (1 + Math.cos(Math.PI * i / (frames - 1))) / 2;
            samples[i] += startCorrection * weight;
            samples[last - i] += endCorrection * weight;
        }
    }
    return buffer;
}

// Loop decoded samples on the audio clock, without restarting a media element.
export class LoopingAudio {
    constructor(url, onLoaded) {
        this.url = url;
        this.onLoaded = onLoaded;
        this.offset = 0;
        this.volume = 1;
        this.muted = false;
    }

    get duration() {
        return this.buffer?.duration || 0;
    }

    get paused() {
        return !this.source;
    }

    get currentTime() {
        if (!this.source) return this.offset;
        return (this.offset + this.context.currentTime - this.startedAt) % this.duration;
    }

    set currentTime(value) {
        const playing = !this.paused;
        this.pause();
        this.offset = this.duration ? Math.max(0, Number(value)) % this.duration : 0;
        if (playing) this.start();
    }

    async play() {
        if (!this.context) {
            this.context = new AudioContext();
            this.gain = this.context.createGain();
            this.gain.connect(this.context.destination);
        }
        // Resume directly from the click, before waiting for the download.
        const resumed = this.context.resume();
        if (!this.loading) {
            this.loading = fetch(this.url)
                .then(response => {
                    if (!response.ok) throw new Error(`Audio download failed: ${response.status}`);
                    return response.arrayBuffer();
                })
                .then(bytes => this.context.decodeAudioData(bytes))
                .then(buffer => {
                    this.buffer = smoothLoopBoundary(buffer);
                    this.onLoaded();
                })
                .catch(error => {
                    this.loading = null;
                    throw error;
                });
        }
        await Promise.all([resumed, this.loading]);
        if (this.paused) this.start();
    }

    start() {
        this.source = this.context.createBufferSource();
        this.source.buffer = this.buffer;
        this.source.loop = true;
        this.source.connect(this.gain);
        this.updateVolume();
        this.startedAt = this.context.currentTime;
        this.source.start(0, this.offset);
    }

    pause() {
        if (!this.source) return;
        this.offset = this.currentTime;
        this.source.stop();
        this.source.disconnect();
        this.source = null;
    }

    updateVolume() {
        if (this.gain) this.gain.gain.setValueAtTime(
            this.muted ? 0 : this.volume, this.context.currentTime
        );
    }
}
