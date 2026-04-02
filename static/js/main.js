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
})
