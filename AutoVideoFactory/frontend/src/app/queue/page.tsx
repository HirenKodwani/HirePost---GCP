"use client";

import { useEffect, useState } from "react";

type JobItem = {
  id: string;
  job_type: string;
  status: string;
  progress: number;
  created_at: string;
};

export default function QueuePage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/jobs/")
      .then((r) => r.json())
      .then((d) => setJobs(d.jobs))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Queue</h1>
      <p className="text-muted-foreground">Job queue and execution status</p>

      {loading ? (
        <div className="text-muted-foreground">Loading...</div>
      ) : (
        <div className="rounded-lg border border-border bg-card">
          <div className="grid grid-cols-6 gap-4 p-4 border-b border-border text-xs font-medium text-muted-foreground uppercase">
            <div className="col-span-2">Job Type</div>
            <div>Status</div>
            <div>Progress</div>
            <div>Created</div>
            <div></div>
          </div>
          {jobs.map((job) => (
            <div key={job.id} className="grid grid-cols-6 gap-4 p-4 border-b border-border/50 text-sm hover:bg-secondary/30">
              <div className="col-span-2 font-medium">{job.job_type}</div>
              <div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor(job.status)}`}>{job.status}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-20 bg-muted rounded-full h-2">
                  <div className="bg-primary h-2 rounded-full" style={{ width: `${job.progress}%` }} />
                </div>
                <span className="text-xs text-muted-foreground">{job.progress}%</span>
              </div>
              <div className="text-muted-foreground text-xs">{new Date(job.created_at).toLocaleString()}</div>
              <div className="text-right">
                <button className="text-xs text-muted-foreground hover:text-foreground">Cancel</button>
              </div>
            </div>
          ))}
          {jobs.length === 0 && (
            <div className="text-center py-12 text-muted-foreground text-sm">No jobs in queue</div>
          )}
        </div>
      )}
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
