"use client";

import { useState } from "react";

type SettingsSection = {
  id: string;
  title: string;
  fields: { key: string; label: string; type: string; value: string }[];
};

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("general");

  const sections: SettingsSection[] = [
    {
      id: "general",
      title: "General",
      fields: [
        { key: "app_name", label: "Application Name", type: "text", value: "AutoVideoFactory" },
        { key: "environment", label: "Environment", type: "select", value: "development" },
        { key: "log_level", label: "Log Level", type: "select", value: "DEBUG" },
      ],
    },
    {
      id: "browser",
      title: "Browser",
      fields: [
        { key: "browser_type", label: "Browser Type", type: "select", value: "chromium" },
        { key: "headless", label: "Headless Mode", type: "boolean", value: "false" },
        { key: "viewport", label: "Viewport Size", type: "text", value: "1280x720" },
      ],
    },
    {
      id: "ai",
      title: "AI Providers",
      fields: [
        { key: "llm_provider", label: "LLM Provider", type: "select", value: "ollama" },
        { key: "llm_model", label: "LLM Model", type: "text", value: "qwen2.5:32b" },
        { key: "ollama_url", label: "Ollama Base URL", type: "text", value: "http://localhost:11434" },
      ],
    },
    {
      id: "publishing",
      title: "Publishing",
      fields: [
        { key: "upload_interval", label: "Upload Interval (s)", type: "number", value: "30" },
        { key: "max_retries", label: "Max Retries", type: "number", value: "3" },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>
      <p className="text-muted-foreground">Application configuration</p>

      <div className="flex gap-6">
        <div className="w-48 flex flex-col gap-1">
          {sections.map((s) => (
            <button
              key={s.id}
              onClick={() => setActiveSection(s.id)}
              className={`text-left px-3 py-2 rounded-md text-sm transition-colors ${
                activeSection === s.id ? "bg-primary/10 text-primary" : "text-muted-foreground hover:text-foreground hover:bg-secondary"
              }`}
            >
              {s.title}
            </button>
          ))}
        </div>

        <div className="flex-1">
          <div className="rounded-lg border border-border bg-card p-6">
            {sections
              .filter((s) => s.id === activeSection)
              .map((s) => (
                <div key={s.id}>
                  <h2 className="text-lg font-semibold mb-4">{s.title}</h2>
                  <div className="space-y-4">
                    {s.fields.map((f) => (
                      <div key={f.key}>
                        <label className="block text-sm text-muted-foreground mb-1">{f.label}</label>
                        {f.type === "boolean" ? (
                          <label className="flex items-center gap-2 cursor-pointer">
                            <div className={`w-10 h-5 rounded-full transition-colors ${f.value === "true" ? "bg-primary" : "bg-muted"} relative`}>
                              <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-all ${f.value === "true" ? "left-5" : "left-0.5"}`} />
                            </div>
                            <span className="text-sm">{f.value === "true" ? "Enabled" : "Disabled"}</span>
                          </label>
                        ) : (
                          <input
                            type={f.type}
                            defaultValue={f.value}
                            className="w-full max-w-md px-3 py-2 bg-secondary rounded-md text-sm border border-border"
                          />
                        )}
                      </div>
                    ))}
                  </div>
                  <button className="mt-6 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm hover:bg-primary/90 transition-colors">
                    Save Changes
                  </button>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}
