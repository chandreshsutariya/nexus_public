const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// User Registration
router.post('/register', authController.register);

// User Login
router.post('/login', authController.login);

// Password Reset
router.post('/reset-password', authController.resetPassword);

// Middleware to protect routes
router.use(authController.authenticate);

// Get User Profile
router.get('/profile', authController.getProfile);

// Update User Profile
router.put('/profile', authController.updateProfile);

// Logout User
router.post('/logout', authController.logout);

module.exports = router;
