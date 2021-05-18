document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault()
    const button = document.getElementById("check")
    button.disabled = true
    button.innerHTML = "<div class=\"spinner-border\" role=\"status\">\n" +
        " <span class=\"visually-hidden\">Loading...</span>\n" +
        "</div>"
    document.querySelector("form").submit()
})
