pokemon_info = JSON;

//for selectionChanged
SELREQUEST = 1;
SELOFFER = 2;

window.onload = (event) => {
    fetch('/tradegetinfo').then(response => response.json()).then(data => { pokemon_info = data; initializeSelects(); });

};

function initializeSelects() {
    selectRequest = document.getElementById("request");
    selectOffer = document.getElementById("offer");

    for (i = 1; i <= 151; i++) {
        opt = document.createElement("option");
        opt2 = document.createElement("option");

        opt.value = i.toString();
        opt2.value = i.toString();

        iPadded = i.toString().padStart(3, '0');
        selection = iPadded + " " + pokemon_info[i].name;
        opt.appendChild(document.createTextNode(selection));
        opt2.appendChild(document.createTextNode(selection));

        selectRequest.appendChild(opt);
        selectOffer.appendChild(opt2);
    }
}

function selectionChanged(sel) {
    if (sel === SELREQUEST) {
        pokeID = document.getElementById("request").value;
        // console.log(pokeID);
        spriteUrl = pokemon_info[pokeID].pokeapiimageurl;
        // console.log(spriteUrl);
        img = document.getElementById("poke1");
        // was super small if I didn't increase sizeborder of image exceeds grid cell, but outer parts of png are empty so doesn't appear to. 
        img.style.width = "70px";
        img.src = spriteUrl;
    } else {
        pokeID = document.getElementById("offer").value;
        // console.log(pokeID);
        spriteUrl = pokemon_info[pokeID].pokeapiimageurl;
        // console.log(spriteUrl);
        img = document.getElementById("poke2");
        // was super small if I didn't increase sizeborder of image exceeds grid cell, but outer parts of png are empty so doesn't appear to. 
        img.style.width = "70px";
        img.src = spriteUrl;
    }
}