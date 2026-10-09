
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null);

  function login(token) {
    setAccessToken(token);
  }

  function updateAccessToken(token) {
    setAccessToken(token);
  }

  function logout() {
    setAccessToken(null);
  }

  const value = {
    accessToken,
    isAuthenticated: Boolean(accessToken),
    login,
    logout,
    updateAccessToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (context === null) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}
