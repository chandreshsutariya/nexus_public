const express = require('express');
const UserController = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');

const router = express.Router();

// User Registration
router.post('/register', UserController.registerUser);

// User Login
router.post('/login', UserController.loginUser);

// Get User Profile
router.get('/profile/:userId', authenticate, UserController.getUserProfile);

// Update User Profile
router.put('/profile/:userId', authenticate, UserController.updateUserProfile);

// Add Friend
router.post('/friends/add/:userId', authenticate, UserController.addFriend);

// Get Friends List
router.get('/friends/:userId', authenticate, UserController.getFriendsList);

// Message Handling (optional)
router.post('/message', authenticate, UserController.sendMessage);
router.get('/messages/:userId', authenticate, UserController.getMessages);

module.exports = router;
