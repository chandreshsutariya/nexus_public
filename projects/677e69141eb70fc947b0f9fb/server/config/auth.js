Here is the code for the `auth.js` file inside `projects/677e69141eb70fc947b0f9fb/server/config/`:

```javascript
const jwt = require('jsonwebtoken');
const User = require('../models/User'); // Adjust the path as needed
require('dotenv').config();

// Middleware for token verification
const verifyToken = (req, res, next) => {
    const token = req.headers['authorization'];

    if (!token) {
        return res.status(403).send('A token is required for authentication');
    }

    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
        if (err) {
            return res.status(401).send('Invalid Token');
        }
        req.user = decoded;
        next();
    });
};

// Middleware for check if user is broadcaster
const isBroadcaster = (req, res, next) => {
    const userRole = req.user.role;
    if (userRole !== 'broadcaster') {
        return res.status(403).send('Access denied. Not a broadcaster.');
    }
    next();
};

// Function to generate JWT token
const generateToken = (user) => {
    return jwt.sign({ id: user._id, role: user.role }, process.env.JWT_SECRET, {
        expiresIn: '24h', // Token expiration time
    });
};

module.exports = {
    verifyToken,
    isBroadcaster,
    generateToken,
};
```