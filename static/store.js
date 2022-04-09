
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
		console.log('Success:', data);
		if (data.error == "not enough points") {
			alert("You don't have enough points");
			console.log("Not enough points");
		}
		else if (data.error == "you already own") {
			alert("You own this item");
			console.log("You have own this pokemon");
		}
		else {
			window.location.reload();
		}
	});

}
