"use client";

import { useEffect, useState } from "react";

type Project = {
  id: string;
  name: string;
  status: string;
  created_at: string;
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/projects/")
      .then((r) => r.json())
      .then((d) => setProjects(d.projects))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Projects</h1>
        <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 transition-colors">
          + New Project
        </button>
      </div>

      {loading ? (
        <div className="text-muted-foreground">Loading...</div>
      ) : projects.length === 0 ? (
        <div className="text-center py-20 text-muted-foreground">
          <div className="text-4xl mb-4 opacity-30">{'\u2630'}</div>
          <p>No projects yet. Create your first project to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-3 gap-4">
          {projects.map((p) => (
            <div key={p.id} className="rounded-lg border border-border bg-card p-4 hover:border-primary/50 transition-colors cursor-pointer">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">{p.name}</h3>
                <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor(p.status)}`}>{p.status}</span>
              </div>
              <p className="text-xs text-muted-foreground">{new Date(p.created_at).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function statusColor(status: string): string {
  const colors: Record<string, string> = {
    draft: "bg-muted text-muted-foreground",
    active: "bg-green-500/10 text-green-400",
    completed: "bg-blue-500/10 text-blue-400",
    archived: "bg-gray-500/10 text-gray-400",
  };
  return colors[status] || "bg-muted text-muted-foreground";
}
