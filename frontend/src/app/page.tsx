import { ProcessingPreviewChart } from "@/components/dashboard/ProcessingPreviewChart";

const publicMetrics = [
  { label: "Average wait", value: "116 days", detail: "sample public cohort" },
  { label: "Recent approvals", value: "2,418", detail: "last 30 days" },
  { label: "Visa bulletin", value: "+3 weeks", detail: "EB2 movement" },
];

const sections = [
  "USCIS processing dashboard",
  "Visa bulletin tracker",
  "Recent approvals",
  "Aggregate timeline trends",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <header className="border-b border-slate-200 bg-white/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
              VisaAtGlance
            </p>
            <p className="text-sm text-slate-500">US visa information, at a glance.</p>
          </div>
          <nav className="hidden items-center gap-6 text-sm font-medium text-slate-600 md:flex">
            <a href="#dashboard">Dashboard</a>
            <a href="#processing">Processing Times</a>
            <a href="#timeline">Timeline</a>
            <a href="#sources">Sources</a>
          </nav>
          <a
            className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-800"
            href="#timeline"
          >
            Compare my timeline
          </a>
        </div>
      </header>

      <section id="dashboard" className="mx-auto grid max-w-7xl gap-8 px-6 py-12 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="flex flex-col justify-center gap-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
            Public immigration data platform
          </p>
          <h1 className="max-w-3xl text-5xl font-semibold leading-tight tracking-normal text-slate-950">
            US visa timelines and bulletin movement in one clear dashboard.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600">
            Explore processing trends, visa bulletin movement, and privacy-safe aggregate timelines without legal advice or approval predictions.
          </p>
          <div className="flex flex-wrap gap-3">
            <a className="rounded-md bg-teal-700 px-5 py-3 text-sm font-semibold text-white" href="#processing">
              Explore public dashboard
            </a>
            <a className="rounded-md border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-800" href="#timeline">
              Compare my timeline
            </a>
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-6 flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-slate-950">Processing preview</h2>
              <p className="text-sm text-slate-500">Aggregated sample trend, not legal guidance.</p>
            </div>
            <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700">
              Public data
            </span>
          </div>
          <ProcessingPreviewChart />
          <dl className="mt-6 grid gap-3 sm:grid-cols-3">
            {publicMetrics.map((metric) => (
              <div key={metric.label} className="rounded-md border border-slate-200 p-4">
                <dt className="text-sm text-slate-500">{metric.label}</dt>
                <dd className="mt-2 text-2xl font-semibold text-slate-950">{metric.value}</dd>
                <p className="mt-1 text-xs text-slate-500">{metric.detail}</p>
              </div>
            ))}
          </dl>
        </div>
      </section>

      <section id="processing" className="border-y border-slate-200 bg-white py-10">
        <div className="mx-auto grid max-w-7xl gap-4 px-6 md:grid-cols-4">
          {sections.map((section) => (
            <div key={section} className="rounded-lg border border-slate-200 p-5">
              <h3 className="text-base font-semibold text-slate-950">{section}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                Source-aware charts with sample size, checked date, and limitations visible near the data.
              </p>
            </div>
          ))}
        </div>
      </section>

      <section id="timeline" className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
          <div>
            <h2 className="text-3xl font-semibold text-slate-950">Enter a timeline, see the cohort context.</h2>
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600">
              The first interaction will compare a user-entered timeline against similar aggregate cases, then ask users to sign in only when they want to save dashboards or alerts.
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 bg-white p-5">
            <p className="text-sm font-semibold text-slate-500">Legal-safe boundary</p>
            <p className="mt-3 text-base leading-7 text-slate-700">
              VisaAtGlance is an informational platform and does not provide legal advice. Always consult official USCIS resources or licensed immigration attorneys for legal guidance.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
