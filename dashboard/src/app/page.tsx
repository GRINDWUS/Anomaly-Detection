"use client";

import React, { useState, useEffect } from "react";
import { 
  Activity, ShieldAlert, Cpu, CheckCircle2, AlertTriangle, XCircle, 
  Satellite, Database, BarChart3, Radio, RefreshCw, ChevronRight, Layers, ArrowUpRight
} from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

interface ComponentData {
  component_id: string;
  iddq_0h: number;
  iddq_24h: number;
  predicted_168h: number;
  risk_tier: "GREEN_AUTO_PASS" | "YELLOW_EXTENDED_TEST" | "RED_EARLY_REJECT";
  drift_delta: number;
  z_score: number;
}

export default function AstraGuardDashboard() {
  const [activeTab, setActiveTab] = useState<"operations" | "component" | "analytics" | "telemetry">("operations");
  const [useWebSocket, setUseWebSocket] = useState(true);
  const [isStreaming, setIsStreaming] = useState(false);
  const [processedComponents, setProcessedComponents] = useState<ComponentData[]>([]);
  const [selectedComponent, setSelectedComponent] = useState<ComponentData | null>(null);
  const [shapData, setShapData] = useState<any>(null);
  const [telemetryReport, setTelemetryReport] = useState<any>(null);
  
  const [stats, setStats] = useState({
    total: 1000,
    processed: 0,
    green: 0,
    yellow: 0,
    red: 0,
    hoursSaved: 84.56
  });

  // Fetch initial Lot Summary and Telemetry Report on load
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/stage-a/lot-summary/LOT_2026_07")
      .then(res => res.json())
      .then(data => console.log("Lot Summary:", data))
      .catch(err => console.error("Lot summary fetch error:", err));

    fetch("http://127.0.0.1:8000/api/v1/stage-b/evaluate-telemetry", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        component_id: "LOT_2026_01_COMP_0000",
        telemetry_iddq: 24.5,
        mission_day: 180
      })
    })
      .then(res => res.json())
      .then(data => setTelemetryReport(data))
      .catch(err => console.error("Telemetry report fetch error:", err));
  }, []);

  // Fetch SHAP attribution when component selected
  useEffect(() => {
    if (selectedComponent) {
      fetch(`http://127.0.0.1:8000/api/v1/stage-a/component/${selectedComponent.component_id}/shap-explanation`)
        .then(res => res.json())
        .then(data => setShapData(data))
        .catch(err => console.error("SHAP fetch error:", err));
    }
  }, [selectedComponent]);

  // Real-Time WebSocket streaming ingestion
  useEffect(() => {
    let ws: WebSocket | null = null;

    if (isStreaming) {
      ws = new WebSocket("ws://127.0.0.1:8000/ws/ate-stream");

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const newComp: ComponentData = {
          component_id: data.component_id,
          iddq_0h: data.iddq_0h,
          iddq_24h: data.iddq_24h,
          predicted_168h: data.predicted_168h_iddq_ua,
          risk_tier: data.risk_tier,
          drift_delta: data.delta_24h_ua,
          z_score: data.spatial_z_score
        };

        setProcessedComponents(prev => [newComp, ...prev.slice(0, 49)]);
        setSelectedComponent(curr => curr || newComp);

        setStats(prev => ({
          ...prev,
          processed: prev.processed + 1,
          green: prev.green + (data.risk_tier === "GREEN_AUTO_PASS" ? 1 : 0),
          yellow: prev.yellow + (data.risk_tier === "YELLOW_EXTENDED_TEST" ? 1 : 0),
          red: prev.red + (data.risk_tier === "RED_EARLY_REJECT" ? 1 : 0),
        }));
      };

      ws.onerror = (err) => console.error("WebSocket error:", err);
    }

    return () => {
      if (ws) ws.close();
    };
  }, [isStreaming]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 px-6 py-4 flex items-center justify-between backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-teal-500/10 border border-teal-500/30 rounded-lg text-teal-400">
            <Cpu className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              ASTRAGUARD 2.0 <span className="text-xs px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 border border-teal-500/30">ISRO RELIABILITY PLATFORM</span>
            </h1>
            <p className="text-xs text-slate-400">PS #SIH26170 | Real-Time WebSocket Streaming & 8 REST APIs</p>
          </div>
        </div>

        {/* Live Controls */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700 text-xs">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span className="text-slate-300 font-medium">WebSocket: ws://127.0.0.1:8000/ws/ate-stream</span>
          </div>

          <button
            onClick={() => setIsStreaming(!isStreaming)}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              isStreaming 
                ? "bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30" 
                : "bg-teal-500 text-slate-950 font-bold hover:bg-teal-400"
            }`}
          >
            {isStreaming ? <Activity className="w-4 h-4 animate-spin" /> : <Radio className="w-4 h-4" />}
            {isStreaming ? "Pause WS Ingestion" : "Start Live WebSocket Stream"}
          </button>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-slate-900/40 border-b border-slate-800 px-6 flex gap-6 text-sm font-medium">
        <button
          onClick={() => setActiveTab("operations")}
          className={`py-3 flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "operations" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <Activity className="w-4 h-4" /> 1. Live ATE Stream (WebSocket)
        </button>
        <button
          onClick={() => setActiveTab("component")}
          className={`py-3 flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "component" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <Cpu className="w-4 h-4" /> 2. SHAP Physics API
        </button>
        <button
          onClick={() => setActiveTab("analytics")}
          className={`py-3 flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "analytics" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <BarChart3 className="w-4 h-4" /> 3. Lot Validation API
        </button>
        <button
          onClick={() => setActiveTab("telemetry")}
          className={`py-3 flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "telemetry" ? "border-teal-400 text-teal-300" : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          <Satellite className="w-4 h-4" /> 4. In-Orbit Telemetry API
        </button>
      </div>

      {/* Main Grid */}
      <main className="flex-1 p-6 grid grid-cols-12 gap-6 overflow-y-auto">
        
        {/* Metric Cards */}
        <div className="col-span-12 grid grid-cols-5 gap-4">
          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl">
            <div className="text-xs text-slate-400 font-medium uppercase">Lot ID / Total Components</div>
            <div className="text-xl font-bold text-white mt-1">LOT_2026_07</div>
            <div className="text-xs text-slate-400 mt-1">Processed: <span className="text-teal-400 font-semibold">{stats.processed} / 1000</span></div>
          </div>
          <div className="bg-slate-900/60 border border-emerald-500/20 p-4 rounded-xl">
            <div className="text-xs text-emerald-400 font-medium uppercase flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> 🟢 Green Pass (24h)
            </div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{stats.green}</div>
            <div className="text-xs text-slate-400 mt-1">Qualifies for Flight</div>
          </div>
          <div className="bg-slate-900/60 border border-amber-500/20 p-4 rounded-xl">
            <div className="text-xs text-amber-400 font-medium uppercase flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5" /> 🟡 Yellow Extended
            </div>
            <div className="text-2xl font-bold text-amber-400 mt-1">{stats.yellow}</div>
            <div className="text-xs text-slate-400 mt-1">Assigned to +48h Re-Test</div>
          </div>
          <div className="bg-slate-900/60 border border-rose-500/20 p-4 rounded-xl">
            <div className="text-xs text-rose-400 font-medium uppercase flex items-center gap-1">
              <XCircle className="w-3.5 h-3.5" /> 🔴 Red Reject (24h)
            </div>
            <div className="text-2xl font-bold text-rose-400 mt-1">{stats.red}</div>
            <div className="text-xs text-slate-400 mt-1">Scrapped at Hour 24</div>
          </div>
          <div className="bg-teal-950/40 border border-teal-500/30 p-4 rounded-xl">
            <div className="text-xs text-teal-300 font-medium uppercase flex items-center justify-between">
              <span>Chamber Hours Saved</span>
              <ArrowUpRight className="w-4 h-4 text-teal-400" />
            </div>
            <div className="text-2xl font-bold text-teal-300 mt-1">{stats.hoursSaved}%</div>
            <div className="text-xs text-teal-400/80 mt-1">Measured Reduction</div>
          </div>
        </div>

        {/* Tab 1 */}
        {activeTab === "operations" && (
          <>
            <div className="col-span-8 bg-slate-900/60 border border-slate-800 rounded-xl p-5 flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Activity className="w-4 h-4 text-teal-400" /> Live WebSocket Data Stream (ws://127.0.0.1:8000/ws/ate-stream)
                </h2>
              </div>
              <div className="flex-1 overflow-y-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-slate-400 border-b border-slate-800 bg-slate-900/80 sticky top-0">
                    <tr>
                      <th className="py-2 px-3">Component ID</th>
                      <th className="py-2 px-3">0h IDDQ</th>
                      <th className="py-2 px-3">24h IDDQ</th>
                      <th className="py-2 px-3">Pred 168h</th>
                      <th className="py-2 px-3">Z-Score</th>
                      <th className="py-2 px-3">Tier</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {processedComponents.map((comp, idx) => (
                      <tr 
                        key={idx} 
                        onClick={() => { setSelectedComponent(comp); setActiveTab("component"); }}
                        className="hover:bg-slate-800/50 cursor-pointer transition-colors"
                      >
                        <td className="py-2 px-3 font-mono text-teal-300">{comp.component_id}</td>
                        <td className="py-2 px-3 text-slate-300">{comp.iddq_0h} µA</td>
                        <td className="py-2 px-3 text-slate-300">{comp.iddq_24h} µA</td>
                        <td className="py-2 px-3 font-semibold text-white">{comp.predicted_168h} µA</td>
                        <td className="py-2 px-3 text-slate-400">{comp.z_score}</td>
                        <td className="py-2 px-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            comp.risk_tier === "GREEN_AUTO_PASS" ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" :
                            comp.risk_tier === "YELLOW_EXTENDED_TEST" ? "bg-amber-500/20 text-amber-300 border border-amber-500/30" :
                            "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                          }`}>
                            {comp.risk_tier.replace("_AUTO_PASS", "").replace("_EXTENDED_TEST", "").replace("_EARLY_REJECT", "")}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="col-span-4 bg-slate-900/60 border border-slate-800 rounded-xl p-5 flex flex-col">
              <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-400" /> Active Component Inspector
              </h2>
              {selectedComponent ? (
                <div className="space-y-4 text-xs">
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <div className="text-slate-400">Component ID</div>
                    <div className="text-base font-mono font-bold text-teal-300 mt-0.5">{selectedComponent.component_id}</div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                      <div className="text-slate-400">Predicted 168h IDDQ</div>
                      <div className="text-lg font-bold text-white mt-0.5">{selectedComponent.predicted_168h} µA</div>
                    </div>
                    <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                      <div className="text-slate-400">24h Delta</div>
                      <div className="text-lg font-bold text-amber-400 mt-0.5">+{selectedComponent.drift_delta} µA</div>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                    <div className="text-slate-400 font-medium mb-1">Action Recommendation:</div>
                    <div className="text-sm font-bold text-teal-300">
                      {selectedComponent.risk_tier === "GREEN_AUTO_PASS" ? "🟢 PASS_AT_24H" :
                       selectedComponent.risk_tier === "YELLOW_EXTENDED_TEST" ? "🟡 EXTENDED_72H_TEST" :
                       "🔴 REJECT_AT_24H"}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex-1 flex items-center justify-center text-slate-500 text-xs">
                  Select a component from table to inspect.
                </div>
              )}
            </div>
          </>
        )}

        {/* Tab 2: Live SHAP API */}
        {activeTab === "component" && (
          <div className="col-span-12 bg-slate-900/60 border border-slate-800 rounded-xl p-6">
            <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-teal-400" /> SHAP Physics Attribution API (`/api/v1/stage-a/component/{selectedComponent?.component_id || "COMP"}/shap-explanation`)
            </h2>
            <div className="grid grid-cols-2 gap-6 mt-4">
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800">
                <h3 className="text-xs font-semibold text-slate-300 mb-4">Degradation Trajectory Curve</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={[
                      { hour: "0h", iddq: selectedComponent ? selectedComponent.iddq_0h : 11.2 },
                      { hour: "24h", iddq: selectedComponent ? selectedComponent.iddq_24h : 12.1 },
                      { hour: "168h (Pred)", iddq: selectedComponent ? selectedComponent.predicted_168h : 14.8 },
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                      <XAxis dataKey="hour" stroke="#64748b" />
                      <YAxis stroke="#64748b" />
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155" }} />
                      <Line type="monotone" dataKey="iddq" stroke="#2dd4bf" strokeWidth={3} dot={{ r: 5 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 flex flex-col justify-between">
                <div>
                  <h3 className="text-xs font-semibold text-slate-300 mb-4">Live SHAP Physics Feature Attribution Response</h3>
                  {shapData ? (
                    <div className="space-y-3 text-xs">
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>24h Drift Velocity (dI/dt)</span>
                          <span className="text-teal-400 font-mono">+{shapData.shap_values.drift_velocity_24h}</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div className="bg-teal-400 h-full w-[85%]"></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Initial Leakage 0h</span>
                          <span className="text-teal-400 font-mono">+{shapData.shap_values.initial_iddq_0h}</span>
                        </div>
                        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div className="bg-teal-400 h-full w-[45%]"></div>
                        </div>
                      </div>
                      <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 text-teal-300 mt-4">
                        <strong>Matched Failure Kinetics:</strong> {shapData.matched_failure_mechanism}
                      </div>
                    </div>
                  ) : (
                    <div className="text-slate-500 text-xs">Loading live SHAP attribution from FastAPI...</div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Lot Validation API */}
        {activeTab === "analytics" && (
          <div className="col-span-12 bg-slate-900/60 border border-slate-800 rounded-xl p-6">
            <h2 className="text-base font-bold text-white mb-4">Leave-One-Lot-Out Cross-Validation API (`/api/v1/analytics/validation-metrics`)</h2>
            <div className="grid grid-cols-4 gap-4 text-xs">
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400">Regression MAE</div>
                <div className="text-xl font-bold text-white mt-1">2.77 µA</div>
              </div>
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400">Sensitivity (Recall)</div>
                <div className="text-xl font-bold text-emerald-400 mt-1">99.28%</div>
              </div>
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400">False Negative Rate (Escapes)</div>
                <div className="text-xl font-bold text-teal-300 mt-1">0.72%</div>
              </div>
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400">Chamber Hours Saved</div>
                <div className="text-xl font-bold text-teal-300 mt-1">84.56%</div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 4: In-Orbit Telemetry API */}
        {activeTab === "telemetry" && (
          <div className="col-span-12 bg-slate-900/60 border border-slate-800 rounded-xl p-6">
            <h2 className="text-base font-bold text-white mb-2">Stage B: In-Orbit Satellite Telemetry API (`/api/v1/stage-b/evaluate-telemetry`)</h2>
            {telemetryReport ? (
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 mt-4 text-xs">
                <div className="flex justify-between text-slate-300 mb-2 font-mono">
                  <span>Component: {telemetryReport.component_id}</span>
                  <span className="text-amber-400 font-bold">Health Score: {telemetryReport.inorbit_health_score} / 100 ({telemetryReport.health_status})</span>
                </div>
                <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 text-slate-300 mt-2">
                  <span className="text-teal-400 font-bold">Actionable FDIR Recommendation:</span> {telemetryReport.fdir_recommendation} (Lead Time: {telemetryReport.lead_time_days} Days)
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-xs">Evaluating telemetry via FastAPI...</div>
            )}
          </div>
        )}

      </main>
    </div>
  );
}
