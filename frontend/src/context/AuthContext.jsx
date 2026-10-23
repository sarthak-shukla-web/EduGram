import { useEffect, useState } from "react";
import AuthContext from "./AuthContextBase";
import {
  loginUser,
  registerUser,
  getCurrentUser,
} from "../services/auth";

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const [loading, setLoading] = useState(
    () => Boolean(localStorage.getItem("access_token"))
  );

  useEffect(() => {
    let cancelled = false;

    const token = localStorage.getItem("access_token");

    if (!token) {
      return;
    }

    const loadUser = async () => {
  try {
    const data = await getCurrentUser();

    if (!cancelled) {
      setUser(data.user);
    }
  } catch (error) {
    console.error("Failed to load current user:", error);

    localStorage.removeItem("access_token");

    if (!cancelled) {
      setUser(null);
    }
  } finally {
    if (!cancelled) {
      setLoading(false);
    }
  }
};
    loadUser();

    return () => {
      cancelled = true;
    };
  }, []);

  const login = async (credentials) => {
    const data = await loginUser(credentials);

    const token = data.access_token || data.token;

    if (token) {
      localStorage.setItem("access_token", token);
    }

    setUser(data.user || data);

    return data;
  };

  const register = async (userData) => {
    const data = await registerUser(userData);
    return data;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthProvider };