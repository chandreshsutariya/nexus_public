Here is the code for the `userController.js` file in the `projects/677e69141eb70fc947b0f9fb/server/controllers/` directory:

```javascript
const User = require('../models/User');

// Create a new user
exports.createUser = async (req, res) => {
    const { name, email, password, role } = req.body;

    try {
        const newUser = new User({
            name,
            email,
            password, // Make sure to hash this before saving in a real application
            role,
        });

        const savedUser = await newUser.save();
        res.status(201).json(savedUser);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

// Retrieve all users
exports.getAllUsers = async (req, res) => {
    try {
        const users = await User.find();
        res.status(200).json(users);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

// Retrieve a user by ID
exports.getUserById = async (req, res) => {
    try {
        const user = await User.findById(req.params.id);
        if (!user) return res.status(404).json({ message: 'User not found' });
        res.status(200).json(user);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

// Update a user
exports.updateUser = async (req, res) => {
    const { name, email, password, role } = req.body;

    try {
        const updatedUser = await User.findByIdAndUpdate(req.params.id, {
            name,
            email,
            password, // Make sure to hash this before saving in a real application
            role,
        }, { new: true });

        res.status(200).json(updatedUser);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

// Delete a user
exports.deleteUser = async (req, res) => {
    try {
        await User.findByIdAndDelete(req.params.id);
        res.status(204).send();
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};
```

Make sure to hash the passwords and handle security properly before saving to the database in a production environment.