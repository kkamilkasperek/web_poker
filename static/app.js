const timeSince = (dateIso) => {
            const date = new Date(dateIso)
            const seconds = Math.floor((new Date() - date) / 1000)
            let interval = seconds / 31536000
            if (interval > 1) {
                return Math.floor(interval) + " years"
            }
            interval = seconds / 2592000
            if (interval > 1) {
                return Math.floor(interval) + " months"
            }
            interval = seconds / 86400
            if (interval > 1) {
                return Math.floor(interval) + " days"
            }
            interval = seconds / 3600
            if (interval > 1) {
                return Math.floor(interval) + " hours"
            }
            interval = seconds / 60
            if (interval > 1) {
                return Math.floor(interval) + " minutes"
            }
            return 0 + " minutes"
}

const updateTimes = () => {
    const dates = document.querySelectorAll('.time-since')
    const regex = /(\d+)\s+minute/
    dates.forEach(date => {
        console.log("function called")
        const time = date.innerText
        const match = time.match(regex)
        if (match) {
            date.innerText = (Number(match[1]) + 1) + " minutes ago"
        }
    })
    // console.log(dates)
}



