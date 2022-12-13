'use strict'

const menuSize = '250px';

let open = true;

document.querySelector('#btnMenu').addEventListener('click', e => {
    open = !open;
    toggleMenu();
})

document.querySelector('#btnClose').addEventListener('click', e => {
    open = false;

    toggleMenu();
})

function toggleMenu() {
    if (open) {
        document.querySelector('#sidebar').style.marginLeft = 0;
        return;
    }

    document.querySelector('#sidebar').style.marginLeft = `-${menuSize}`;
}




document.querySelectorAll('.options a').forEach(link => {
link.onclick = function (e) {
    e.preventDefault()

    const conteudo = document.getElementById('conteudo')
    fetch(link.href)
    .then(resp => resp.text())
    .then(html => (conteudo.innerHTML = html))
}
})



function redireciona(){
var search = document.getElementById("search").value;
location.href="{% url 'swenergy:index' %}" + search;
}

