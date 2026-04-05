document.addEventListener("alpine:init", () => {
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
