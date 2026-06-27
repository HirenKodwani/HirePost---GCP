"use client";

import { useEffect, useState } from "react";

type DashboardData = {
  stats: {
    total_projects: number;
    total_jobs: number;
    active_jobs: number;
    failed_jobs: number;
    completed_jobs: number;
  };
  recent_jobs: Array<{
    id: string;
    job_type: string;
    status: string;
    progress: number;
    created_at: string;
  }>;
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/admin/dashboard")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-full text-muted-foreground">Loading...</div>;
  }

  if (!data) {
    return <div className="text-destructive">Failed to load dashboard</div>;
  }

  const { stats } = data;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex gap-2">
          <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">Online</span>
          <span className="px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">v0.1.0</span>
        </div>
      </div>

      <div className="grid grid-cols-5 gap-4">
        <StatCard title="Projects" value={stats.total_projects} color="blue" />
        <StatCard title="Total Jobs" value={stats.total_jobs} color="green" />
        <StatCard title="Active" value={stats.active_jobs} color="yellow" />
        <StatCard title="Completed" value={stats.completed_jobs} color="emerald" />
        <StatCard title="Failed" value={stats.failed_jobs} color="red" />
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <div className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-lg font-semibold mb-4">Recent Jobs</h2>
            <div className="space-y-2">
              {data.recent_jobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-3 rounded-md bg-secondary/50">
                  <div>
                    <div className="text-sm font-medium">{job.job_type}</div>
                    <div className="text-xs text-muted-foreground">{new Date(job.created_at).toLocaleString()}</div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-24 bg-muted rounded-full h-2">
                      <div className="bg-primary h-2 rounded-full" style={{ width: `${job.progress}%` }} />
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor(job.status)}`}>{job.status}</span>
                  </div>
                </div>
              ))}
              {data.recent_jobs.length === 0 && (
                <div className="text-muted-foreground text-sm py-8 text-center">No jobs yet</div>
              )}
            </div>
          </div>
        </div>

        <div>
          <div className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-lg font-semibold mb-4">System</h2>
            <div className="space-y-3">
              <SystemInfo label="CPU" value="-" />
              <SystemInfo label="Memory" value="-" />
              <SystemInfo label="Storage" value="-" />
              <SystemInfo label="GPU" value="-" />
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-4 mt-4">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-2">
              <button className="w-full text-left px-3 py-2 rounded-md bg-primary/10 text-primary text-sm hover:bg-primary/20 transition-colors">
                New Project
              </button>
              <button className="w-full text-left px-3 py-2 rounded-md bg-secondary text-sm hover:bg-secondary/80 transition-colors">
                Generate Video
              </button>
              <button className="w-full text-left px-3 py-2 rounded-md bg-secondary text-sm hover:bg-secondary/80 transition-colors">
                Run Pipeline
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }: { title: string; value: number; color: string }) {
  const colors: Record<string, string> = {
    blue: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    green: "bg-green-500/10 text-green-400 border-green-500/20",
    yellow: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    red: "bg-red-500/10 text-red-400 border-red-500/20",
  };

  return (
    <div className={`rounded-lg border p-4 ${colors[color] || colors.blue}`}>
      <div className="text-sm opacity-80">{title}</div>
      <div className="text-3xl font-bold mt-1">{value}</div>
    </div>
  );
}

function SystemInfo({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-muted-foreground">{label}</span>
      <span>{value}</span>
    </div>
  );
}

function statusColor(status: string): string {
  const colors: Record<string, string> = {
    pending: "bg-yellow-500/10 text-yellow-400",
    running: "bg-blue-500/10 text-blue-400",
    completed: "bg-green-500/10 text-green-400",
    failed: "bg-red-500/10 text-red-400",
    cancelled: "bg-gray-500/10 text-gray-400",
  };
  return colors[status] || "bg-muted text-muted-foreground";
}
