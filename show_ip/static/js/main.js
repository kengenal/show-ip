const input = document.getElementById("address").parentElement.parentElement.innerHTML

document.querySelector("#add-address").addEventListener("click", () => {
    document.querySelector("#addresses").innerHTML += input
})

function removeItem(e) {
    const elem = document.querySelectorAll("#address")
    if (elem.length !== 1){
        e.parentElement.remove()
    }
}
