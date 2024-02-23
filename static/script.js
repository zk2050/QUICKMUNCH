// script.js
fetch('/restaurants')
  .then(response => response.json())
  .then(data => {
    data.forEach(restaurant => {
      // Create HTML elements and populate them with restaurant data
      const restaurantElement = document.createElement('div');
      restaurantElement.className = 'grid-item';

      const titleElement = document.createElement('h2');
      titleElement.textContent = restaurant.title;
      restaurantElement.appendChild(titleElement);

      const priceElement = document.createElement('h3');
      priceElement.textContent = restaurant.price;
      restaurantElement.appendChild(priceElement);

      const imageElement = document.createElement('img');
      imageElement.src = restaurant.image_path;
      // Append imageElement to the appropriate location in your HTML
      // For example:
      // document.getElementById('store-image-box').appendChild(imageElement);

      // Append restaurantElement to the appropriate location in your HTML
      // For example:
      // document.getElementById('container').appendChild(restaurantElement);
    });
  })
  .catch(error => console.error('Error fetching restaurants:', error));
