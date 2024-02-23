fetch('/restaurants')
  .then(response => response.json())
  .then(data => {
    data.forEach(restaurant => {
      // Create HTML elements and populate them with restaurant data
      const restaurantElement = document.createElement('div');
      restaurantElement.className = 'grid-item';

      const nameElement = document.createElement('h2');
      nameElement.textContent = restaurant.name;
      restaurantElement.appendChild(nameElement);

      const ratingElement = document.createElement('h3');
      ratingElement.textContent = restaurant.rating;
      restaurantElement.appendChild(ratingElement);

      const imageElement = document.createElement('div');
      imageElement.id = 'store-image-box'; // Assign id to the image container div
      imageElement.style.backgroundImage = `url('${restaurant.image_url}')`; // Set background image
      restaurantElement.appendChild(imageElement);

      // Append restaurantElement to the appropriate location in your HTML
      // For example:
      document.getElementById('container').appendChild(restaurantElement);
    });
  })
  .catch(error => console.error('Error fetching restaurants:', error));