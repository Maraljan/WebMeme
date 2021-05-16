function toggleElements(className, hidden = false) {
    let elements = document.getElementsByClassName(className)
    for (let element of elements) {
        element.hidden = hidden
    }
}