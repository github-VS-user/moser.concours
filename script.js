const API_URL = "https://moserconcours-backend.onrender.com";

async function chargerEleves() {
    let response = await fetch(API_URL + "/eleves");
    let data = await response.json();
    
    let liste = document.getElementById("listeEleves");
    liste.innerHTML = "";
    
    data.forEach(eleve => {
        let row = `<tr><td>${eleve.nom}</td><td>${eleve.points}</td></tr>`;
        liste.innerHTML += row;
    });
}

chargerEleves();

function loginEleve() {
    window.location.href = "dashboard.html";
}

function loginAdmin() {
    let password = prompt("Entrez le mot de passe admin :");
    if (password === "admin123") {
        window.location.href = "admin.html";
    } else {
        alert("Mot de passe incorrect !");
    }
}
