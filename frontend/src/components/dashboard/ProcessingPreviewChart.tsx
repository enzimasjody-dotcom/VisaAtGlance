"use client";

import dynamic from "next/dynamic";

const DynamicProcessingPreviewChart = dynamic(
  () =>
    import("./ProcessingPreviewChartInner").then(
      (module) => module.ProcessingPreviewChartInner,
    ),
  {
    ssr: false,
    loading: () => <div className="h-64 w-full rounded-md bg-slate-100" />,
  },
);

export function ProcessingPreviewChart() {
  return <DynamicProcessingPreviewChart />;
}
