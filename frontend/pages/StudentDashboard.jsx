import { useEffect, useState } from "react";
import { getDashboard } from "../api/api";

export default function Dashboard({ user }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (user?.user_id) {
      getDashboard(user.user_id).then((res) => {
        setData(res.data);
      });
    }
  }, [user]);

  if (!data) return <div>Loading dashboard...</div>;

  return (
    <div style={{ padding: 30 }}>
      <h2>Welcome {user.name}</h2>

      <div>
        <h3>Stats</h3>
        <p>Total Submissions: {data.stats.total_submissions}</p>
        <p>Evaluated: {data.stats.evaluated}</p>
        <p>Average Score: {data.stats.average_score.toFixed(2)}</p>      </div>

      <h3>Submissions</h3>
      {data.submissions.map((s, i) => (
        <div key={i} style={{ border: "1px solid gray", margin: 10 }}>
          <p>Video: {s.video_id}</p>
          <p>Status: {s.status}</p>
        </div>
      ))}
    </div>
  );
}