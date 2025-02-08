const API_URL = "https://moserconcours-backend.onrender.com";

// 🔑 Function to login admin
async function loginAdmin() {
    let username = document.getElementById("adminUsername").value;
    let password = document.getElementById("adminPassword").value;

    let response = await fetch(API_URL + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    let result = await response.json();
    if (response.ok) {
        localStorage.setItem("token", result.access_token);
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("adminPanel").style.display = "block";
        chargerEleves();
    } else {
        alert("Identifiants incorrects !");
    }
}

// 🚪 Function to logout admin
function logoutAdmin() {
    localStorage.removeItem("token");
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("adminPanel").style.display = "none";
}

// 📥 Function to load student data
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

// ➕ Function to add points
async function ajouterPoints() {
    let token = localStorage.getItem("token");
    let nom = document.getElementById("nomEleve").value;
    let points = parseInt(document.getElementById("points").value);

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

// ➖ Function to remove points
async function retirerPoints() {
    let token = localStorage.getItem("token");
    let nom = document.getElementById("nomEleve").value;
    let points = parseInt(document.getElementById("points").value) * -1;

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

// 🔄 Auto-check if admin is logged in
document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("token")) {
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("adminPanel").style.display = "block";
        chargerEleves();
    }
});
