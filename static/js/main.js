document.addEventListener("alpine:init", () => {
    Alpine.data("videoList", () => ({
        videos: [],

        async init() {
            this.videos = await (await fetch('/videos')).json()
            const videoEvents = new EventSource('/videos/events')
            videoEvents.onmessage = async () => {
                this.videos = await (await fetch('/videos')).json()
            }
        }
    }))

    Alpine.data("videoCard", () => ({
        async playVideo(video) {
            console.log(video);
            await fetch('/play', {
                method: "POST",
                body: new URLSearchParams({
                    file: video.title
                })
            })
        }
    }))

    Alpine.data("downloadBar", () => ({
        url: "",

        async download() {
            await fetch("download", {
                method: "POST",
                body: new URLSearchParams({
                    url: this.url
                })
            })
        }
    }))
})
