import { useState, useEffect, useCallback } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import { getStatus } from "./api";

export default function App() {
  const [status, setStatus] = useState(null);
  const [toast, setToast] = useState(null);

  /* ---- Fetch backend status ---- */
  const refreshStatus = useCallback(async () => {
    try {
      const data = await getStatus();
      setStatus(data);
    } catch {
      setStatus(null);
    }
  }, []);

  useEffect(() => {
    refreshStatus();
    const interval = setInterval(refreshStatus, 10000); // poll every 10s
    return () => clearInterval(interval);
  }, [refreshStatus]);

  /* ---- Toast helper ---- */
  const showToast = (message, type = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  return (
    <div className="app-layout">
      <Sidebar
        status={status}
        onToast={showToast}
        refreshStatus={refreshStatus}
      />
      <ChatPanel status={status} />

      {/* Toast */}
      {toast && (
        <div className={`toast toast-${toast.type}`}>{toast.message}</div>
      )}
    </div>
  );
}
