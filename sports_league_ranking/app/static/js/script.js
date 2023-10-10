// script.js

document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tabs li a");
    tabs.forEach(tab => {
        tab.addEventListener("click", function(event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const sections = document.querySelectorAll("section");
            console.log(targetId, sections)
            sections.forEach(section => {
                section.style.display = "none";
            });
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = "block";
            }
            // document.getElementById(targetId).style.display = "block";
        });
    });
});
