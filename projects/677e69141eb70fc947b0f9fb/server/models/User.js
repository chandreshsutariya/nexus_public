Here's the code for the `User.js` model file located in `projects/677e69141eb70fc947b0f9fb/server/models/User.js`:

```javascript
const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
    },
    password: {
        type: String,
        required: true,
    },
    role: {
        type: String,
        enum: ['male', 'female', 'broadcaster'],
        required: true,
    },
    coins: {
        type: Number,
        default: 0,
    },
    verified: {
        type: Boolean,
        default: false,
    },
});

module.exports = mongoose.model('User', UserSchema);
```