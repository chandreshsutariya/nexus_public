Here is the code for the file `projects/677e69141eb70fc947b0f9fb/server/routes/userRoutes.js`:

```javascript
const express = require('express');
const userController = require('../controllers/userController');
const router = express.Router();

// User registration
router.post('/register', userController.registerUser);

// User login
router.post('/login', userController.loginUser);

// Get user profile
router.get('/profile/:id', userController.getUserProfile);

// Update user profile
router.put('/profile/:id', userController.updateProfile);

// Delete user account
router.delete('/account/:id', userController.deleteAccount);

// Get all users (for admin purposes)
router.get('/', userController.getAllUsers);

module.exports = router;
```