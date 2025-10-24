import apiClient from "./apiClient";

export const uploadCSV = async (formData: FormData, userId: string) => {
  const response = await apiClient.post(`/ingestion/upload?user_id=${userId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};
