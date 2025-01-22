Here is the code for the file `projects/677e69141eb70fc947b0f9fb/server/config/db.js`:

```javascript
const mongoose = require('mongoose');
require('dotenv').config();

const connectDB = async () => {
    try {
        await mongoose.connect(process.env.MONGODB_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log('MongoDB connected');
    } catch (err) {
        console.error(err.message);
        process.exit(1);  // Exit process with failure
    }
};

module.exports = connectDB;
```