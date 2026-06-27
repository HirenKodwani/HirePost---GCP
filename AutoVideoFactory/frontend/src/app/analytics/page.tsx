"use client";

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>
      <p className="text-muted-foreground">Video performance analytics and insights</p>

      <div className="grid grid-cols-4 gap-4">
        <MetricCard title="Total Views" value="0" change="+" />
        <MetricCard title="Total Likes" value="0" change="+" />
        <MetricCard title="Avg Watch %" value="0%" change="+" />
        <MetricCard title="Followers Gained" value="0" change="+" />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="rounded-lg border border-border bg-card p-4">
          <h2 className="text-sm font-semibold mb-4 uppercase text-muted-foreground">Performance Over Time</h2>
          <div className="h-64 flex items-center justify-center text-muted-foreground text-sm">
            No data yet. Publish videos to see analytics.
          </div>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <h2 className="text-sm font-semibold mb-4 uppercase text-muted-foreground">Top Performing Content</h2>
          <div className="h-64 flex items-center justify-center text-muted-foreground text-sm">
            No data yet.
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, change }: { title: string; value: string; change: string }) {
  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <div className="text-sm text-muted-foreground">{title}</div>
      <div className="text-2xl font-bold mt-1">{value}</div>
      <div className="text-xs text-muted-foreground mt-1">{change}% vs last period</div>
    </div>
  );
}
