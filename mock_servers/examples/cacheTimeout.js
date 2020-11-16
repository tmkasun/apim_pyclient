(
    () => {

        fetch('http://localhost:8000/apis', { cache: "default" });
        const intID = setInterval(() => console.log("Waiting . . ."), 1000);
        setTimeout(() => {
            fetch('http://localhost:8000/apis', { cache: "default" })
                .then(res => clearInterval(intID));

        }, 5000)
    })()

    (
        () => {

            fetch('http://localhost:8000/apis', { cache: "default" });
            const intID = setInterval(() => console.log("Waiting . . ."), 1000);
            const reqInt = setInterval(() => {
                fetch('http://localhost:8000/apis', { cache: "default" })
                    .then(res => clearInterval(intID));

            }, 4000)
        })()
