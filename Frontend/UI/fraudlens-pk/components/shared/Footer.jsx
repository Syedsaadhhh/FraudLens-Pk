import { Shield, Github } from "lucide-react";
import { GITHUB_URL } from "@/data/dummyData";

export function Footer() {
  return (
    <footer className="border-t border-white/10">
      <div className="max-w-7xl mx-auto px-5 md:px-8 py-10 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-accent" />
          <span className="text-sm text-slate-300 font-medium">FraudLens PK</span>
          <span className="text-sm text-slate-600">·</span>
          <span className="text-sm text-slate-500">Made for Pakistan</span>
        </div>
        <div className="flex items-center gap-6 text-sm text-slate-500">
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 hover:text-accent transition-colors"
          >
            <Github className="w-4 h-4" /> GitHub
          </a>
          <span>Hackathon 2026</span>
        </div>
      </div>
    </footer>
  );
}
