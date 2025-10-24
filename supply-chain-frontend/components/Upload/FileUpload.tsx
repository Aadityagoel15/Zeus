import { useState } from "react";
import { uploadCSV } from "../../src/api/ingestionAPI";
import { useUser } from "@clerk/clerk-react";

const FileUpload: React.FC = () => {
  const { user } = useUser();
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file || !user) {
      alert("Select a CSV file and ensure you're logged in!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await uploadCSV(formData, user.id);
      alert("Upload successful!");
      console.log(response);
    } catch (err) {
      console.error(err);
      alert("Upload failed!");
    }
  };

  return (
    <div className="p-6 border rounded-lg max-w-lg mx-auto mt-10">
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
      />
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
      >
        Upload
      </button>
    </div>
  );
};

export default FileUpload;
