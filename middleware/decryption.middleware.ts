import { decrypt, encrypt } from "../utils/crypto";
import { Request, Response, NextFunction } from "express";

export const decryptionMiddleware = (req: Request, res: Response, next: NextFunction): void => {
    try {
        if (req.headers.env && req.headers.env === "test") {
            next();
        } else if (req.body && Object.keys(req.body).length > 0) {
            if (req.body.mac && req.body.value) {
                // Decrypt the request body here
                const decrypted = decrypt(req.body); // Assuming decrypt is defined in the utils/crypto module
                req.body = JSON.parse(decrypted); // Parse decrypted data to replace the body
                next(); // Proceed with the request
            } else {
                res.status(500).send({ error: "Encrypt data required. Ex: { mac, value }" });
            }
        } else {
            next();
        }
    } catch (error) {
        console.error("Decryption failed:", error);
        res.status(500).send({ error: "Decrypt data is required." });
    }
};
