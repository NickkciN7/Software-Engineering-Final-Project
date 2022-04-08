window.onload = (event) => {
	for (i = 1; i <= 151; i++) {

		button = document.getElementById(i.toString());
		button.onclick = function () { purchase(i); };
	}
};

function purchase(pokeid) {
	console.log(pokeid);

	// const dataToSend = { id: pokeid };
	// fetch('/purchasepokemon', {
	// 	method: 'POST',
	// 	headers: {
	// 		'Content-Type': 'application/json',
	// 	},
	// 	body: JSON.stringify(dataToSend),
	// }).then(response => response.json()).then(data => {
	// 	console.log('Success:', data);
	// });
}
