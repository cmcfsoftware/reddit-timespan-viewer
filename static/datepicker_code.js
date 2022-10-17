function showTVShowHelper() {
    let helper = document.getElementById('TVShowHelper');
    //p.removeAttribute("hidden");
    if (helper.style.display === "none") {
        helper.style.display = "block";
    } else {
        helper.style.display = "none";
    }
}