
window.onload = (event) => {

	for (i = 1; i <= 151; i++) {
		// buttonid = i;
		// console.log(buttonid);
		button = document.getElementById(i);
		// pokeid_array.push(i);
		// console.log(button.innerText);
		// console.log(pokeid_array[i - 1]);
		(function (index) {
			button.addEventListener("click", function () {
				purchase(index);
			})
		})(i)

	}
};

function purchase(pokeid) {
	// console.log(pokeid);

	const dataToSend = { id: pokeid };
	fetch('/purchasepokemon', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(dataToSend),
	}).then(response => response.json()).then(data => {
		if (data.error == "not enough points") {
			alert("You don't have enough points");
			console.log("Not enough points");
		}
		if (data.error == "already in collection") {
			alert("You already own this pokemon");
			console.log("You have own this pokemon");
		}
		if (data.success == "pokemon purchased") {
			alert("You have purchased this pokemon");
			console.log("success");
		
		}
		console.log("here");
		window.location.reload();
	});

}
