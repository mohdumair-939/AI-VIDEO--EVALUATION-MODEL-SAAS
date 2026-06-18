import { useState, useEffect } from "react";
import { getTasks, uploadVideo, evaluateVideo, getEvaluation } from "../api/api";

export default function Upload({ user }) {
  const [file, setFile] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [taskId, setTaskId] = useState("");
  const [videoId, setVideoId] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    getTasks().then((res) => setTasks(res.data.tasks));
  }, []);

  // -------------------------
  // POLLING ENGINE (IMPORTANT SaaS FEATURE)
  // -------------------------
  useEffect(() => {
    let interval;

    if (videoId) {
      interval = setInterval(async () => {
        const res = await getEvaluation(videoId);

        if (res.data.success) {
          setResult(res.data.data);
          clearInterval(interval);
        }
      }, 3000);
    }

    return () => clearInterval(interval);
  }, [videoId]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("task_id", taskId);
    formData.append("user_id", user.user_id);

    const res = await uploadVideo(formData);

    setVideoId(res.data.video_id);

    await evaluateVideo(res.data.video_id);
  };

  return (
    <div style={{ padding: 30 }}>
      <h2>Upload Task Video</h2>

      <select onChange={(e) => setTaskId(e.target.value)}>
        <option value="">Select Task</option>
        {tasks.map((t) => (
          <option key={t.task_id} value={t.task_id}>
            {t.title}
          </option>
        ))}
      </select>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        Submit
      </button>

      {/* ---------------- RESULTS ---------------- */}
      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Result</h3>
          <p>Score: {result.result.final_score}</p>
          <p>Status: {result.result.status}</p>
          <p>Grade: {result.result.grade}</p>
        </div>
      )}
    </div>
  );
}