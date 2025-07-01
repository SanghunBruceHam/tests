
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 5000;

// Serve static files from the egen-teto/ko directory
app.use(express.static(path.join(__dirname, 'egen-teto/ko')));

// Route for the main application
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'egen-teto/ko/index.html'));
});

// Handle other routes by serving the appropriate HTML files
app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'egen-teto/ko/about.html'));
});

app.get('/test', (req, res) => {
  res.sendFile(path.join(__dirname, 'egen-teto/ko/test.html'));
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
