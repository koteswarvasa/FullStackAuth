
import { apiRequest } from "./api";

export function registerUser(userData) {
  return apiRequest("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify(userData),
  });
}

export function loginUser(credentials) {
  return apiRequest("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}
