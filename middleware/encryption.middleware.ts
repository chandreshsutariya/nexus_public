import { encrypt } from "../utils/crypto";
import { Request, Response, NextFunction } from "express";

export const encryptionMiddleware = (req: Request, res: Response, next: NextFunction): any => {
  // Override res.json to include encryption logic
  res.json = ((body: Record<string, unknown> | any[]) => {
    try {
      // Encrypt the response body
      const encrypted = encrypt(JSON.stringify(body));
      
      // Send the encrypted response
      return encrypted;
    } catch (error) {
      console.error("Encryption failed:", error);
      res.status(500).send({ error: "Failed to encrypt the response." });
    }

    return res;
  }) as any;

  next();
};
