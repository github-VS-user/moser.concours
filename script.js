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

async function ajouterPoints(nom, points) {
    let token = localStorage.getItem("token");
    let response = await fetch(API_URL + "/ajouter_points", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ nom, points })
    });

    let result = await response.json();
    alert(result.message);
    chargerEleves();
}

async function loginAdmin() {
    let username = prompt("Nom d'utilisateur admin :");
    let password = prompt("Mot de passe :");

    let response = await fetch(API_URL + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    let result = await response.json();
    if (response.ok) {
        localStorage.setItem("token", result.access_token);
        window.location.href = "admin.html";
    } else {
        alert("Identifiants incorrects !");
    }
}

chargerEleves();
