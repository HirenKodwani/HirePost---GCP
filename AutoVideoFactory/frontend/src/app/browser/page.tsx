"use client";

import { useState } from "react";

export default function BrowserPage() {
  const [url, setUrl] = useState("https://");
  const [sessions] = useState([
    { id: "1", name: "TikTok Upload", active: false },
    { id: "2", name: "YouTube Studio", active: false },
    { id: "3", name: "Kling AI", active: false },
  ]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Browser</h1>
      <p className="text-muted-foreground">Browser automation sessions and live view</p>

      <div className="grid grid-cols-4 gap-4">
        <div className="col-span-1">
          <div className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-sm font-semibold mb-3 uppercase text-muted-foreground">Sessions</h2>
            <div className="space-y-2">
              {sessions.map((s) => (
                <div key={s.id} className="flex items-center gap-3 p-2 rounded-md hover:bg-secondary cursor-pointer">
                  <div className={`w-2 h-2 rounded-full ${s.active ? "bg-green-500" : "bg-muted"}`} />
                  <span className="text-sm">{s.name}</span>
                </div>
              ))}
              <button className="w-full text-sm text-primary mt-2 hover:underline">+ New Session</button>
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-4 mt-4">
            <h2 className="text-sm font-semibold mb-3 uppercase text-muted-foreground">Controls</h2>
            <div className="space-y-2">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full px-3 py-2 bg-secondary rounded-md text-sm border border-border"
              />
              <button className="w-full px-3 py-2 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 transition-colors">
                Navigate
              </button>
              <button className="w-full px-3 py-2 bg-secondary text-sm rounded-md hover:bg-secondary/80 transition-colors">
                Screenshot
              </button>
              <button className="w-full px-3 py-2 bg-secondary text-sm rounded-md hover:bg-secondary/80 transition-colors">
                Save Session
              </button>
            </div>
          </div>
        </div>

        <div className="col-span-3">
          <div className="rounded-lg border border-border bg-card h-[600px] flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <div className="text-4xl mb-2 opacity-30">{'\u25C9'}</div>
              <p className="text-sm">Browser viewport</p>
              <p className="text-xs mt-1">Launch a browser session to see the live view</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
