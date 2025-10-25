const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api";

export async function fetchData(endpoint: string) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("API fetch error:", error);
    throw error;
  }
}
