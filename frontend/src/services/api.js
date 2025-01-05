const API_URL = "http://127.0.0.1:8000";

export const login = async (username, password) => {
    const response = await fetch(`${API_URL}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    // console.log(response.json())
    if (!response.ok) throw new Error("Invalid credentials");
    return await response.json();
};
