"use client";

import { useEffect, useState } from "react";

type AgentInfo = {
  name: string;
  status: string;
  capabilities: string[];
  current_task: string | null;
  queue_size: number;
};

export default function AgentsPage() {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/agents/")
      .then((r) => r.json())
      .then((d) => setAgents(d.agents))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Agents</h1>
      <p className="text-muted-foreground">Multi-agent system status and control</p>

      {loading ? (
        <div className="text-muted-foreground">Loading...</div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {agents.map((agent) => (
            <div key={agent.name} className="rounded-lg border border-border bg-card p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${agent.status === "running" ? "bg-green-500" : agent.status === "failed" ? "bg-red-500" : "bg-muted"}`} />
                  <h3 className="font-semibold capitalize">{agent.name}</h3>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor(agent.status)}`}>{agent.status}</span>
              </div>
              <div className="flex flex-wrap gap-1 mb-3">
                {agent.capabilities.map((cap) => (
                  <span key={cap} className="text-xs px-2 py-0.5 rounded-full bg-secondary text-muted-foreground">{cap}</span>
                ))}
              </div>
              <div className="text-xs text-muted-foreground">
                <div>Queue: {agent.queue_size} tasks</div>
                <div>Current Task: {agent.current_task || "None"}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function statusColor(status: string): string {
  const colors: Record<string, string> = {
    idle: "bg-muted text-muted-foreground",
    running: "bg-green-500/10 text-green-400",
    completed: "bg-blue-500/10 text-blue-400",
    failed: "bg-red-500/10 text-red-400",
    cancelled: "bg-gray-500/10 text-gray-400",
    waiting: "bg-yellow-500/10 text-yellow-400",
  };
  return colors[status] || "bg-muted text-muted-foreground";
}
