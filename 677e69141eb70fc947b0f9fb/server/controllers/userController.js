```javascript
const User = require('../models/User');

// User registration
exports.registerUser = async (req, res) => {
    const { name, email, password, accountType } = req.body;
    try {
        const newUser = new User({ name, email, password, accountType });
        await newUser.save();
        res.status(201).json({ message: 'User registered successfully', userId: newUser._id });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};

// User login
exports.loginUser = async (req, res) => {
    const { email, password } = req.body;
    try {
        const user = await User.findOne({ email });
        if (!user || !(await user.comparePassword(password))) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }
        res.status(200).json({ message: 'Login successful', userId: user._id });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// Get user profile
exports.getUserProfile = async (req, res) => {
    const userId = req.params.id;
    try {
        const user = await User.findById(userId);
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// Update user profile
exports.updateUserProfile = async (req, res) => {
    const userId = req.params.id;
    const updates = req.body;
    try {
        const user = await User.findByIdAndUpdate(userId, updates, { new: true });
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.status(200).json({ message: 'Profile updated successfully', user });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};

// Delete user account
exports.deleteUserAccount = async (req, res) => {
    const userId = req.params.id;
    try {
        const user = await User.findByIdAndDelete(userId);
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.status(200).json({ message: 'User account deleted successfully' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
```