
window.onload = (event) => {

	for (i = 1; i <= 151; i++) {
		button = document.getElementById(i);
		(function (index) {
			button.addEventListener("click", function () {
				purchase(index);
			})
		})(i)

	}
};

function purchase(pokeid) {
	const dataToSend = { id: pokeid };
	fetch('/purchasepokemon', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(dataToSend),
	}).then(response => response.json()).then(data => {
		if (data < "NotEnoughPoints") {
			alert("You haven't earned enough points yet!")
			console.log(data);
		}


	});

}
