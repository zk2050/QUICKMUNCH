// server.js
const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

const db = new sqlite3.Database('restaurants.db');

// Define your routes and database interactions here
// Example:
app.get('/restaurants', (req, res) => {
  db.all('SELECT * FROM restaurants', [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json(rows);
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
