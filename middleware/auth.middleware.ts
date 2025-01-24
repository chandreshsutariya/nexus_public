import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import { getAppString, sendError } from "../utils/response";
import redis from "../config/redis";
import Admin, { IAdmin } from "../modules/admin/admin.model";
import { UserType } from "../utils/enums";
import Agency, { IAgency } from "../modules/agency/agency.model";

export const verifyAccessToken = (requiredUserType?: string) => {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const lang: any = req.headers.lang || "en";
    try {
      const authHeader = req.headers.authorization;

      if (!authHeader || !authHeader.startsWith("Bearer ")) {
        sendError(req, res, { token: getAppString("tokenRequired", lang) }, 401);
        return;
      }

      const token = authHeader.split(" ")[1];
      const secret = process.env.JWT_ACCESS_SECRET || "b4f577d2aa9cc60f9e9912761c6a907067a3f6f4f241f3111d957b0486c73d04a0aaf1824507a609813232888c26ec7de01193afb100993e2cd7e6ab8b3a99d3";
      
      const isBlacklisted = await redis.get(`blacklist:${token}`);
      if (isBlacklisted) {
        sendError(req, res, { token: getAppString("tokenNotValid", lang) }, 401);
        return;
      }

      // Verify the token
      const decoded = jwt.verify(token, secret) as { userId: string; userType: string };
      (req as any).user = decoded; // Attach decoded token payload to the request object

      if (decoded.userType === "admin") {
        const subAdmin: any = await Admin.findById(decoded.userId); // Fetch the sub-admin using the userId from the token
       
        // Check if the sub-admin's account is inactive (status = false)
        if (subAdmin && subAdmin.status === false) {
          sendError(req, res, { general: getAppString("accountDeactivatedsubadmin", lang) }, 403); // Return error if account is deactivated
          return;
        }
      }

      if (decoded.userType === "agency") {
        const subAdmin: any = await Agency.findById(decoded.userId); // Fetch the sub-admin using the userId from the token
       
        // Check if the sub-admin's account is inactive (status = false)
        if (subAdmin && subAdmin.status === false) {
          sendError(req, res, { general: getAppString("accountDeactivatedsubadmin", lang) }, 403); // Return error if account is deactivated
          return;
        }
      }
      
      // Check userType if required
      if (requiredUserType && decoded.userType !== requiredUserType) {
        sendError(req, res, { token: "Unauthorized access." }, 401);
        return;
      }

      next();
    } catch (error) {
      console.log("Error_verifyAccessToken", error);
      sendError(req, res, { token: "Invalid or expired access token." }, 401);
    }
  };
};

// New Middleware: verifyAccessTokens for multiple user types
export const verifyAccessTokens = (requiredUserTypes: string[]) => {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const lang: any = req.headers.lang || "en";
    try {
      const authHeader = req.headers.authorization;

      if (!authHeader || !authHeader.startsWith("Bearer ")) {
        sendError(req, res, { token: getAppString("tokenRequired", lang) }, 401);
        return;
      }

      const token = authHeader.split(" ")[1];
      const secret = process.env.JWT_ACCESS_SECRET || "your-secret-key";

      const isBlacklisted = await redis.get(`blacklist:${token}`);
      if (isBlacklisted) {
        sendError(req, res, { token: getAppString("tokenNotValid", lang) }, 401);
        return;
      }

      // Verify the token
      const decoded = jwt.verify(token, secret) as { userId: string; userType: string };
      (req as any).user = decoded; // Attach decoded token payload to the request object

      // Check if the user's account is deactivated (if admin)
      if (decoded.userType === UserType.ADMIN) {
        const subAdmin: any = await Admin.findById(decoded.userId); // Fetch the sub-admin using the userId from the token

        // Check if the sub-admin's account is inactive (status = false)
        if (subAdmin && subAdmin.status === false) {
          sendError(req, res, { general: getAppString("accountDeactivatedsubadmin", lang) }, 403); // Return error if account is deactivated
          return;
        }
      }

      if (decoded.userType === UserType.AGENCY) {
        const subAdmin: any = await Agency.findById(decoded.userId); // Fetch the sub-admin using the userId from the token
       
        // Check if the sub-admin's account is inactive (status = false)
        if (subAdmin && subAdmin.status === false) {
          sendError(req, res, { general: getAppString("accountDeactivatedsubadmin", lang) }, 403); // Return error if account is deactivated
          return;
        }
      }

      // Check if the user's userType is in the allowed array of user types
      if (!requiredUserTypes.includes(decoded.userType)) {
        sendError(req, res, { token: "Unauthorized access." }, 401);
        return;
      }

      next();
    } catch (error) {
      console.log("Error_verifyAccessTokens", error);
      sendError(req, res, { token: "Invalid or expired access token." }, 401);
    }
  };
};