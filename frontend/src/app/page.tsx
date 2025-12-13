"use client";

import { useState, useRef, useEffect } from "react";

interface ProgressUpdate {
  step: string;
  message: string;
  percent: number;
  data: any;
}

interface Intelligence {
  level: number;
  xp: number;
  stage_name: string;
  stage_emoji: string;
  stage_desc: string;
  total_projects: number;
  total_files: number;
  languages: string[];
  next_stage: { name: string; emoji: string; xp_needed: number } | null;
}

interface Skill {
  id: string;
  name: string;
  icon: string;
  unlocked: boolean;
}

interface SkillStage {
  name: string;
  level_min: number;
  unlocked: boolean;
  current: boolean;
  skills: Skill[];
}

interface SkillTree {
  stages: SkillStage[];
  current_stage: string;
  unlocked_count: number;
  total_count: number;
  progress_percent: number;
}

interface CodeError {
  line: number;
  code_snippet: string;
  error_type: string;
  message: string;
  explanation: string;
  fix: string | null;
}

interface AgentResult {
  idea: string;
  plan: any;
  code_files: string[];
  all_code: Record<string, string>;
  final_code: string;
  review: {
    has_errors?: boolean;
    errors?: CodeError[];
    summary?: string;
    score?: number;
  };
  xp_gained?: number;
  intelligence?: Intelligence;
  learned_from: boolean;
  extras?: { tests: string; cicd: string; dockerfile: string };
}

interface Template {
  id: string;
  name: string;
  icon: string;
  description: string;
  prompt: string;
  tags: string[];
}

interface MemoryProject {
  id: number;
  idea: string;
  xp_gained: number;
  languages: string[];
  file_count: number;
  files: string[];
  quality_score: number;
  timestamp: string;
}

export default function Home() {
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState<ProgressUpdate | null>(null);
  const [result, setResult] = useState<AgentResult | null>(null);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [intelligence, setIntelligence] = useState<Intelligence | null>(null);
  const [skillTree, setSkillTree] = useState<SkillTree | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [memory, setMemory] = useState<MemoryProject[]>([]);
  const [isListening, setIsListening] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [showSkillTree, setShowSkillTree] = useState(false);
  const [showMemory, setShowMemory] = useState(false);
  const [rateLimited, setRateLimited] = useState(false);
  const [deployUrl, setDeployUrl] = useState("");
  const [explaining, setExplaining] = useState(false);
  const [explanations, setExplanations] = useState<{ line: number; code: string; explanation: string }[]>([]);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/intelligence").then(r => r.json()).then(setIntelligence).catch(() => { });
    fetch("http://localhost:8000/skills").then(r => r.json()).then(setSkillTree).catch(() => { });
    fetch("http://localhost:8000/templates").then(r => r.json()).then(setTemplates).catch(() => { });
    fetch("http://localhost:8000/memory").then(r => r.json()).then(setMemory).catch(() => { });
    fetch("http://localhost:8000/status").then(r => r.json()).then(d => setRateLimited(d.rate_limited)).catch(() => { });
  }, []);

  const refreshData = () => {
    fetch("http://localhost:8000/intelligence").then(r => r.json()).then(setIntelligence).catch(() => { });
    fetch("http://localhost:8000/skills").then(r => r.json()).then(setSkillTree).catch(() => { });
  };

  const startVoice = () => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) { alert("Voice input requires Chrome or Edge browser"); return; }
    setIsListening(true);
    const recognition = new SR();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.onresult = (event: any) => {
      setIdea((prev) => prev + (prev ? " " : "") + event.results[0][0].transcript);
      setIsListening(false);
    };
    recognition.onerror = (event: any) => {
      setIsListening(false);
      if (event.error === "not-allowed") alert("Microphone access denied.");
      else if (event.error === "network") alert("Network error. Speech requires internet.");
    };
    recognition.onend = () => setIsListening(false);
    try { recognition.start(); } catch { setIsListening(false); }
  };

  const getPreviewSrc = () => {
    if (!result?.all_code) return "";

    // Find HTML file
    let h = result.all_code["index.html"] || "";
    if (!h) {
      // Try to find any HTML file
      const htmlFile = Object.keys(result.all_code).find(f => f.endsWith(".html"));
      if (htmlFile) h = result.all_code[htmlFile];
    }
    if (!h) return "";

    // Find CSS file
    let c = result.all_code["styles.css"] || result.all_code["style.css"] || "";
    if (!c) {
      const cssFile = Object.keys(result.all_code).find(f => f.endsWith(".css"));
      if (cssFile) c = result.all_code[cssFile];
    }

    // Find JS file
    let j = result.all_code["main.js"] || result.all_code["script.js"] || "";
    if (!j) {
      const jsFile = Object.keys(result.all_code).find(f => f.endsWith(".js"));
      if (jsFile) j = result.all_code[jsFile];
    }

    // Build complete HTML - DON'T strip body, just inject CSS/JS
    let fullHtml = h;

    // If HTML has head, inject CSS there
    if (h.includes("</head>")) {
      fullHtml = h.replace("</head>", `<style>${c}</style></head>`);
    } else {
      fullHtml = `<!DOCTYPE html><html><head><style>${c}</style></head><body>${h}</body></html>`;
    }

    // If HTML has body end, inject JS there
    if (fullHtml.includes("</body>")) {
      fullHtml = fullHtml.replace("</body>", `<script>${j}</script></body>`);
    }

    return `data:text/html;charset=utf-8,${encodeURIComponent(fullHtml)}`;
  };

  const run = async (improve: boolean = false) => {
    const targetIdea = improve && result?.idea ? result.idea : idea;
    if (!targetIdea.trim()) return;
    setLoading(true); setProgress(null); setResult(null); setSelectedFile("");
    abortRef.current = new AbortController();
    try {
      const res = await fetch("http://localhost:8000/run-stream", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: targetIdea, improve }), signal: abortRef.current.signal,
      });
      const reader = res.body?.getReader();
      const dec = new TextDecoder();
      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;
        for (const line of dec.decode(value).split("\n")) {
          if (line.startsWith("data: ")) {
            try {
              const u: ProgressUpdate = JSON.parse(line.slice(6));
              setProgress(u);
              if (u.data?.intelligence) setIntelligence(u.data.intelligence);
              if (u.step === "complete" && u.data) {
                const d = u.data as AgentResult;
                setResult(d);
                if (d.code_files?.length) setSelectedFile(d.code_files[0]);
                if (d.intelligence) setIntelligence(d.intelligence);
                refreshData();
              }
            } catch { }
          }
        }
      }
    } catch { } finally { setLoading(false); }
  };

  const hasWeb = result?.code_files?.some(f => f.endsWith(".html"));

  return (
    <div className="min-h-screen bg-[#000] text-[#fafafa] antialiased">
      {/* Nav */}
      <nav className="h-12 border-b border-[#1a1a1a] flex items-center justify-between px-5">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-[#7c3aed] to-[#4f46e5]" />
            <span className="text-sm font-medium tracking-tight">autogenesis</span>
          </div>
          <div className="h-4 w-px bg-[#262626]" />
          <button onClick={() => { setShowSkillTree(!showSkillTree); setShowMemory(false); }} className="text-xs text-[#737373] hover:text-white transition">
            Skills
          </button>
          <button onClick={() => { setShowMemory(!showMemory); setShowSkillTree(false); }} className="text-xs text-[#737373] hover:text-white transition">
            Memory
          </button>
        </div>
        <div className="flex items-center gap-4">
          {intelligence && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-[#525252]">Level {intelligence.level}%</span>
              <div className="w-20 h-1 bg-[#1a1a1a] rounded-full overflow-hidden">
                <div className="h-full bg-[#7c3aed] transition-all" style={{ width: `${intelligence.level}%` }} />
              </div>
            </div>
          )}
          <a href="http://localhost:8000/export" className="text-xs text-[#525252] hover:text-white transition">Export</a>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-5 pt-8 pb-20">
        {/* Rate Limit Banner */}
        {rateLimited && (
          <div className="mb-4 px-4 py-2.5 rounded-lg bg-yellow-500/10 border border-yellow-500/30 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-yellow-400">⚠️</span>
              <span className="text-xs text-yellow-400">API rate limited - Using demo mode with sample outputs</span>
            </div>
            <span className="text-[10px] text-yellow-400/60">Resets in ~1 hour</span>
          </div>
        )}

        {/* Skill Tree Modal */}
        {showSkillTree && skillTree && (
          <div className="mb-6 rounded-lg border border-[#1a1a1a] bg-[#0a0a0a] overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-[#1a1a1a]">
              <div>
                <span className="text-sm font-medium">AI Skill Tree</span>
                <span className="ml-2 text-xs text-[#525252]">{skillTree.unlocked_count}/{skillTree.total_count} skills</span>
              </div>
              <button onClick={() => setShowSkillTree(false)} className="text-xs text-[#525252] hover:text-white">Close</button>
            </div>

            {/* Skill Tree Visual */}
            <div className="p-4 overflow-x-auto">
              <div className="flex gap-1 min-w-max">
                {skillTree.stages.map((stage, i) => (
                  <div key={stage.name} className="flex items-center">
                    {/* Stage */}
                    <div className={`relative p-3 rounded-lg border transition-all duration-500 ${stage.current ? "border-[#7c3aed] bg-[#7c3aed]/10" :
                      stage.unlocked ? "border-[#22c55e]/50 bg-[#22c55e]/5" : "border-[#262626] bg-[#0a0a0a]"
                      }`}>
                      <div className="text-center mb-2">
                        <div className={`text-lg ${stage.unlocked ? "" : "grayscale opacity-50"}`}>
                          {stage.name === "Baby" && "👶"}
                          {stage.name === "Child" && "🧒"}
                          {stage.name === "Teen" && "🧑"}
                          {stage.name === "Adult" && "🧑‍💼"}
                          {stage.name === "Expert" && "🧙"}
                          {stage.name === "Sage" && "🏆"}
                        </div>
                        <div className={`text-[10px] font-medium ${stage.current ? "text-[#7c3aed]" : stage.unlocked ? "text-[#22c55e]" : "text-[#525252]"}`}>
                          {stage.name}
                        </div>
                        <div className="text-[8px] text-[#404040]">Lvl {stage.level_min}+</div>
                      </div>

                      {/* Skills */}
                      <div className="flex flex-wrap gap-1 justify-center max-w-[100px]">
                        {stage.skills.map(skill => (
                          <div
                            key={skill.id}
                            title={skill.name}
                            className={`w-6 h-6 rounded flex items-center justify-center text-xs transition-all duration-300 ${skill.unlocked
                              ? "bg-[#1a1a1a] hover:scale-110 cursor-default"
                              : "bg-[#0a0a0a] grayscale opacity-30"
                              }`}
                          >
                            {skill.icon}
                          </div>
                        ))}
                      </div>

                      {/* Current indicator */}
                      {stage.current && (
                        <div className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-[#7c3aed] animate-pulse" />
                      )}
                    </div>

                    {/* Connector */}
                    {i < skillTree.stages.length - 1 && (
                      <div className={`w-4 h-0.5 ${skillTree.stages[i + 1].unlocked ? "bg-[#22c55e]/50" : "bg-[#262626]"
                        }`} />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Progress bar */}
            <div className="px-4 pb-3">
              <div className="flex justify-between text-[10px] text-[#525252] mb-1">
                <span>Skill Progress</span>
                <span>{skillTree.progress_percent}%</span>
              </div>
              <div className="h-1 bg-[#1a1a1a] rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#7c3aed] to-[#22c55e] transition-all duration-500"
                  style={{ width: `${skillTree.progress_percent}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Memory View */}
        {showMemory && (
          <div className="mb-6 rounded-lg border border-[#1a1a1a] bg-[#0a0a0a] overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-[#1a1a1a]">
              <div>
                <span className="text-sm font-medium">Project Memory</span>
                <span className="ml-2 text-xs text-[#525252]">{memory.length} projects</span>
              </div>
              <button onClick={() => setShowMemory(false)} className="text-xs text-[#525252] hover:text-white">Close</button>
            </div>
            {memory.length === 0 ? (
              <div className="p-6 text-center text-sm text-[#525252]">No projects yet. Generate your first!</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead className="bg-[#0f0f0f]">
                    <tr>
                      <th className="px-3 py-2 text-left text-[#525252]">#</th>
                      <th className="px-3 py-2 text-left text-[#525252]">Project</th>
                      <th className="px-3 py-2 text-left text-[#525252]">XP</th>
                      <th className="px-3 py-2 text-left text-[#525252]">Languages</th>
                      <th className="px-3 py-2 text-left text-[#525252]">Files</th>
                      <th className="px-3 py-2 text-left text-[#525252]">Quality</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1a1a1a]">
                    {memory.map((p) => (
                      <tr key={p.id} className="hover:bg-[#141414]">
                        <td className="px-3 py-2 text-[#404040]">{p.id}</td>
                        <td className="px-3 py-2 text-[#a3a3a3] max-w-[180px] truncate">{p.idea}</td>
                        <td className="px-3 py-2 text-emerald-400">+{p.xp_gained}</td>
                        <td className="px-3 py-2">
                          {p.languages.map((l) => (
                            <span key={l} className="mr-1 px-1.5 py-0.5 bg-[#1a1a1a] rounded text-[10px] text-[#737373]">{l}</span>
                          ))}
                        </td>
                        <td className="px-3 py-2 text-[#525252]">{p.file_count}</td>
                        <td className="px-3 py-2">
                          <span className={p.quality_score >= 8 ? "text-emerald-400" : "text-yellow-400"}>{p.quality_score}/10</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Hero */}
        <div className="text-center mb-4">
          <h1 className="text-3xl font-semibold tracking-tight mb-2 bg-gradient-to-r from-white via-[#a78bfa] to-white bg-clip-text text-transparent">
            Code Generation
          </h1>
          <p className="text-sm text-[#737373]">Describe your project or pick a template</p>
        </div>

        {/* Templates */}
        {templates.length > 0 && !result && (
          <div className="mb-4">
            <div className="flex gap-2 flex-wrap justify-center">
              {templates.map((t) => (
                <button
                  key={t.id}
                  onClick={() => setIdea(t.prompt)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-[#262626] bg-[#0a0a0a] text-xs text-[#a3a3a3] hover:border-[#7c3aed] hover:text-white transition"
                  title={t.description}
                >
                  <span>{t.icon}</span>
                  <span>{t.name}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="rounded-lg border border-[#1a1a1a] bg-[#0a0a0a] overflow-hidden mb-6">
          <textarea
            className="w-full bg-transparent p-4 text-sm text-white placeholder-[#404040] resize-none focus:outline-none"
            rows={3}
            placeholder="Build a calculator with HTML, CSS, and JavaScript..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            disabled={loading}
          />
          <div className="flex items-center justify-between px-4 py-3 border-t border-[#1a1a1a]">
            <button
              onClick={startVoice}
              className={`text-xs px-2.5 py-1 rounded transition ${isListening ? "bg-red-500/20 text-red-400" : "text-[#525252] hover:text-white"}`}
            >
              {isListening ? "Listening..." : "Voice input"}
            </button>
            <button
              onClick={loading ? () => abortRef.current?.abort() : () => run(false)}
              disabled={!idea.trim() && !loading}
              className="text-xs font-medium px-4 py-1.5 rounded bg-white text-black hover:bg-[#e5e5e5] disabled:opacity-30 transition"
            >
              {loading ? "Cancel" : "Generate"}
            </button>
          </div>
        </div>

        {/* Progress */}
        {loading && progress && (
          <div className="mb-6">
            <div className="flex justify-between text-xs mb-1.5">
              <span className="text-[#737373]">{progress.message}</span>
              <span className="text-[#525252] font-mono">{progress.percent}%</span>
            </div>
            <div className="h-0.5 bg-[#1a1a1a] rounded-full overflow-hidden">
              <div className="h-full bg-[#7c3aed] transition-all" style={{ width: `${progress.percent}%` }} />
            </div>
          </div>
        )}

        {/* XP Gain + Actions */}
        {result?.xp_gained && (
          <div className="mb-4 flex items-center justify-between flex-wrap gap-2">
            <span className="text-xs text-[#737373]">
              +{result.xp_gained} XP earned{intelligence?.next_stage ? ` · ${intelligence.next_stage.xp_needed}% to next level` : ""}
            </span>
            <div className="flex gap-2">
              <button
                onClick={async () => {
                  const code = result.all_code?.[selectedFile] || "";
                  if (!code) return;
                  setExplaining(true);
                  try {
                    const res = await fetch("http://localhost:8000/explain", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({ code, language: selectedFile.split(".").pop() || "Python" })
                    });
                    const data = await res.json();
                    setExplanations(data.explanations || []);
                  } catch { setExplanations([]); }
                  setExplaining(false);
                }}
                disabled={explaining}
                className="text-xs px-3 py-1.5 rounded border border-[#525252] text-[#737373] hover:border-white hover:text-white transition"
              >
                {explaining ? "..." : "💡 Explain"}
              </button>
              <button
                onClick={async () => {
                  const res = await fetch("http://localhost:8000/deploy", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ project_name: result.plan?.project_name || "autogenesis" })
                  });
                  const data = await res.json();
                  if (data.url) setDeployUrl(data.url);
                }}
                className="text-xs px-3 py-1.5 rounded border border-emerald-500/50 text-emerald-400 hover:bg-emerald-500 hover:text-white transition"
              >
                🚀 Deploy to Vercel
              </button>
              <button
                onClick={() => run(true)}
                disabled={loading}
                className="text-xs px-3 py-1.5 rounded border border-[#7c3aed] text-[#7c3aed] hover:bg-[#7c3aed] hover:text-white transition disabled:opacity-30"
              >
                Build Again, But Better
              </button>
            </div>
          </div>
        )}

        {/* Deploy URL */}
        {deployUrl && (
          <div className="mb-4 px-4 py-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-emerald-400">✓</span>
              <span className="text-xs text-emerald-400">Deployed!</span>
              <a href={deployUrl} target="_blank" className="text-xs text-white underline">{deployUrl}</a>
            </div>
            <button onClick={() => setDeployUrl("")} className="text-xs text-emerald-400/60 hover:text-white">×</button>
          </div>
        )}

        {/* Explanations Panel */}
        {explanations.length > 0 && (
          <div className="mb-4 rounded-lg border border-[#1a1a1a] bg-[#0a0a0a] overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2 border-b border-[#1a1a1a]">
              <span className="text-xs font-medium text-[#a78bfa]">💡 Code Explanation</span>
              <button onClick={() => setExplanations([])} className="text-xs text-[#525252] hover:text-white">Close</button>
            </div>
            <div className="divide-y divide-[#1a1a1a]">
              {explanations.map((e, i) => (
                <div key={i} className="px-4 py-2 flex gap-3">
                  <span className="text-[10px] text-[#404040] w-6">L{e.line}</span>
                  <code className="text-xs text-[#737373] font-mono flex-1 truncate">{e.code}</code>
                  <span className="text-xs text-[#a3a3a3]">{e.explanation}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-4">
            {/* Code Panel with Line Numbers */}
            <div className="rounded-lg border border-[#1a1a1a] overflow-hidden">
              <div className="flex items-center border-b border-[#1a1a1a] bg-[#0a0a0a]">
                <div className="flex flex-1">
                  {result.code_files?.map((f) => (
                    <button
                      key={f}
                      onClick={() => setSelectedFile(f)}
                      className={`px-4 py-2.5 text-xs transition border-b-2 -mb-px ${selectedFile === f
                        ? "border-[#7c3aed] text-white"
                        : "border-transparent text-[#525252] hover:text-[#a3a3a3]"
                        }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
                {result.review?.score && (
                  <span className={`mx-2 text-[10px] px-2 py-0.5 rounded ${result.review.score >= 8 ? "bg-emerald-500/20 text-emerald-400" :
                    result.review.score >= 5 ? "bg-yellow-500/20 text-yellow-400" :
                      "bg-red-500/20 text-red-400"
                    }`}>
                    Quality: {result.review.score}/10
                  </span>
                )}
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(result.all_code?.[selectedFile] || "");
                    const btn = document.getElementById("copy-btn");
                    if (btn) { btn.textContent = "Copied!"; setTimeout(() => btn.textContent = "Copy", 1500); }
                  }}
                  id="copy-btn"
                  className="px-3 py-2 text-[10px] text-[#525252] hover:text-white transition"
                >
                  Copy
                </button>
              </div>
              <div className="bg-[#050505] overflow-auto h-64">
                <table className="w-full">
                  <tbody>
                    {(result.all_code?.[selectedFile] || "").split("\n").map((line, i) => {
                      const lineNum = i + 1;
                      const error = result.review?.errors?.find(e => e.line === lineNum);
                      return (
                        <tr key={i} className={error ? "bg-red-500/10" : ""}>
                          <td className="px-2 py-0.5 text-[10px] text-[#404040] select-none text-right border-r border-[#1a1a1a] w-8">
                            {lineNum}
                          </td>
                          <td className="px-3 py-0.5 text-xs font-mono text-[#a3a3a3] whitespace-pre">
                            {line || " "}
                            {error && (
                              <span className="ml-2 text-[10px] text-red-400">← {error.message}</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Error Panel */}
            {result.review?.has_errors && result.review.errors && result.review.errors.length > 0 && (
              <div className="rounded-lg border border-red-500/30 bg-red-500/5 overflow-hidden">
                <div className="px-4 py-2.5 border-b border-red-500/20 bg-red-500/10 flex items-center justify-between">
                  <div>
                    <span className="text-xs text-red-400 font-medium">
                      {result.review.errors.length} Issue{result.review.errors.length > 1 ? "s" : ""} Found
                    </span>
                    <span className="text-[10px] text-[#525252] ml-2">
                      {result.review.errors.map(e => `Line ${e.line}`).join(", ")}
                    </span>
                  </div>
                  <button
                    onClick={async () => {
                      const code = result.all_code?.[selectedFile] || "";
                      const errors = result.review?.errors?.map(e => e.message).join("; ") || "";
                      const res = await fetch("http://localhost:8000/fix", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ code, error: errors })
                      });
                      const data = await res.json();
                      if (data.fixed_code) {
                        setResult({
                          ...result,
                          all_code: { ...result.all_code, [selectedFile]: data.fixed_code },
                          review: { ...result.review, has_errors: false, errors: [], score: 10 }
                        });
                      }
                    }}
                    className="text-xs px-3 py-1.5 rounded bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500 hover:text-white transition font-medium"
                  >
                    Fix All & Improve
                  </button>
                </div>
                <div className="p-3 text-xs text-[#737373] space-y-1">
                  {result.review.errors.slice(0, 3).map((err, i) => (
                    <div key={i} className="flex gap-2">
                      <span className="text-red-400">Line {err.line}:</span>
                      <span>{err.message}</span>
                    </div>
                  ))}
                  {result.review.errors.length > 3 && (
                    <div className="text-[#525252]">+ {result.review.errors.length - 3} more issues</div>
                  )}
                </div>
              </div>
            )}

            {/* Preview Panel */}
            {hasWeb && (
              <div className="rounded-lg border border-[#1a1a1a] overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2.5 bg-[#0a0a0a] border-b border-[#1a1a1a]">
                  <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#ef4444]" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#eab308]" />
                    <div className="w-2.5 h-2.5 rounded-full bg-[#22c55e]" />
                  </div>
                  <div className="flex-1 mx-4">
                    <div className="bg-[#1a1a1a] rounded px-3 py-1 text-[10px] text-[#525252] text-center">localhost:preview</div>
                  </div>
                  <button onClick={() => setShowPreview(!showPreview)} className="text-[10px] text-[#525252] hover:text-white transition">
                    {showPreview ? "Hide" : "Show"}
                  </button>
                </div>
                {showPreview && (
                  <div className="bg-white aspect-video max-h-80">
                    <iframe src={getPreviewSrc()} className="w-full h-full border-0" sandbox="allow-scripts" />
                  </div>
                )}
              </div>
            )}

            {/* Extras */}
            {result.extras && (
              <div className="flex items-center gap-3 text-xs text-[#525252]">
                <span className="text-[#737373]">Also generated:</span>
                <span className="px-2 py-1 bg-[#1a1a1a] rounded">Tests</span>
                <span className="px-2 py-1 bg-[#1a1a1a] rounded">CI/CD</span>
                <span className="px-2 py-1 bg-[#1a1a1a] rounded">Dockerfile</span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
