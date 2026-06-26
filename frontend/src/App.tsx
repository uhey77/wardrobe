import { CheckCircle2, Database, RefreshCw, Server, Shirt } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

type Phase0Response = {
  message: string;
  next_phase: string;
};

type PingState =
  | { status: "idle"; data?: undefined; error?: undefined }
  | { status: "loading"; data?: undefined; error?: undefined }
  | { status: "success"; data: Phase0Response; error?: undefined }
  | { status: "error"; data?: undefined; error: string };

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export function App() {
  const [pingState, setPingState] = useState<PingState>({ status: "idle" });

  const pingBackend = useCallback(async () => {
    setPingState({ status: "loading" });

    try {
      const response = await fetch(`${apiBaseUrl}/api/phase0`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = (await response.json()) as Phase0Response;
      setPingState({ status: "success", data });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      setPingState({ status: "error", error: message });
    }
  }, []);

  useEffect(() => {
    void pingBackend();
  }, [pingBackend]);

  const isLoading = pingState.status === "loading";

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="app-title">
        <header className="topbar">
          <div className="brand">
            <span className="brand-icon" aria-hidden="true">
              <Shirt size={22} strokeWidth={2.1} />
            </span>
            <div>
              <h1 id="app-title">Wardrobe</h1>
              <p>Phase 0</p>
            </div>
          </div>
          <span className="status-pill">
            <CheckCircle2 size={16} />
            Skeleton Ready
          </span>
        </header>

        <div className="status-grid">
          <article className="status-panel">
            <div className="panel-heading">
              <Server size={20} />
              <h2>Backend</h2>
            </div>
            <p className="endpoint">{apiBaseUrl}/api/phase0</p>
            <div className={`result result-${pingState.status}`}>
              {pingState.status === "idle" && "Waiting"}
              {pingState.status === "loading" && "Checking"}
              {pingState.status === "success" && pingState.data.message}
              {pingState.status === "error" && pingState.error}
            </div>
            <button type="button" onClick={() => void pingBackend()} disabled={isLoading}>
              <RefreshCw size={16} className={isLoading ? "spin" : undefined} />
              Ping API
            </button>
          </article>

          <article className="status-panel">
            <div className="panel-heading">
              <Database size={20} />
              <h2>ChromaDB</h2>
            </div>
            <p className="endpoint">localhost:8001</p>
            <div className="result result-idle">Configured</div>
            <span className="command-label">task chroma:up</span>
          </article>
        </div>
      </section>
    </main>
  );
}
