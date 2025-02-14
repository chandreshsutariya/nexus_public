
const crypto = require('crypto');

const algorithm = 'aes-256-cbc';

const encrypt = (req, res, next) => {
    const key
 = Buffer.from(process.env.ENC_KEY_CLIENT, 'hex');
    const iv = Buffer.from(process.env.ENC_IV_CLIENT, 'hex');

    res.oldJson = res.json;
    res.json = (data) => {
        if (req.headers.env === 'test') {
            // No encryption in test environment
            res.oldJson(data); // Send data as is
            return; // Important: Exit the function to prevent further execution
        }
        const json = JSON.stringify(data);
        const cipher = crypto.createCipheriv(algorithm, key
, iv);
        let encrypted = cipher.update(json, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        res.oldJson({ encrypted });
    };

    next();
};

const decrypt = (req, res, next) => {
    if (req.body && req.body.encrypted) {
        const key
 = Buffer.from(process.env.ENC_KEY_SERVER, 'hex');
        const iv = Buffer.from(process.env.ENC_IV_SERVER, 'hex');

        const decipher = crypto.createDecipheriv(algorithm, key
, iv);
        let decrypted = decipher.update(req.body.encrypted, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        req.body = JSON.parse(decrypted);
    }
    next();
};

module.exports = {
    encrypt,
    decrypt,
};