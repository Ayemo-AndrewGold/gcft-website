"use client";

import { useDeferredValue, useEffect, useRef, useState } from "react";
import { resources, resourceTabs, searchSuggestions, type ResourceType } from "@/lib/content";
import { Container, Eyebrow, Icon, SectionTitle, linkProps } from "./ui";

const typeStyle: Record<ResourceType, { badge: string; icon: string; cta: string; ctaIcon: string }> = {
  audio: { badge: "bg-primary/10 text-primary", icon: "headphones", cta: "Listen", ctaIcon: "play_circle" },
  guides: { badge: "bg-surface-container-high text-secondary", icon: "menu_book", cta: "Read", ctaIcon: "arrow_forward" },
  video: { badge: "bg-error-container/20 text-error", icon: "play_circle", cta: "Watch", ctaIcon: "smart_display" },
};

export default function ArchivesSection() {
  const [query, setQuery] = useState("");
  const [type, setType] = useState<"all" | ResourceType>("all");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const boxRef = useRef<HTMLDivElement>(null);
  const deferred = useDeferredValue(query);

  // ⌘K / Ctrl+K focuses search; outside click closes suggestions.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === "Escape") setShowSuggestions(false);
    };
    const onClick = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setShowSuggestions(false);
    };
    window.addEventListener("keydown", onKey);
    document.addEventListener("mousedown", onClick);
    return () => {
      window.removeEventListener("keydown", onKey);
      document.removeEventListener("mousedown", onClick);
    };
  }, []);

  const q = deferred.toLowerCase().trim();
  const visible = resources.filter(
    (r) =>
      (type === "all" || r.type === type) &&
      (!q || [r.title, r.body, r.author, r.keywords, r.kind].join(" ").toLowerCase().includes(q)),
  );

  return (
    <section id="archives" className="w-full bg-surface-container-lowest py-section">
      <Container>
        <div className="mb-space-lg flex flex-col justify-between gap-space-md md:flex-row md:items-end">
          <div>
            <Eyebrow variant="dot" className="mb-space-xs">
              GCFT Media
            </Eyebrow>
            <SectionTitle>Sermon Library</SectionTitle>
          </div>

          {/* Search */}
          <div ref={boxRef} className="relative w-full md:w-96">
            <div className="relative flex items-center">
              <Icon name="search" className="pointer-events-none absolute left-space-sm text-on-surface-variant" />
              <input
                ref={inputRef}
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onFocus={() => setShowSuggestions(true)}
                placeholder="Search sermons, articles, topics..."
                aria-label="Search library"
                className="w-full rounded-lg border border-on-surface/15 bg-surface-container-low py-2.5 pr-20 pl-10 text-body-sm text-on-surface placeholder:text-[#8e95a5] focus:border-primary-container focus:ring-1 focus:ring-primary-container/35 focus:outline-none [&::-webkit-search-cancel-button]:hidden"
              />
              <div className="absolute right-2 flex items-center gap-1">
                {query && (
                  <button
                    type="button"
                    aria-label="Clear search"
                    onClick={() => {
                      setQuery("");
                      inputRef.current?.focus();
                    }}
                    className="p-1 text-on-surface-variant hover:text-on-surface"
                  >
                    <Icon name="close" size={16} />
                  </button>
                )}
                <kbd className="hidden rounded bg-surface-container-high px-1.5 py-0.5 text-[10px] font-semibold text-on-surface-variant md:inline-block">
                  ⌘K
                </kbd>
              </div>
            </div>
            {showSuggestions && (
              <div className="glass-2 absolute top-full right-0 left-0 z-30 mt-1 rounded-xl p-space-sm shadow-2xl">
                <span className="mb-1 block px-space-xs text-label-sm uppercase tracking-wider text-on-surface-variant">
                  Popular Queries
                </span>
                <div className="flex flex-wrap gap-1">
                  {searchSuggestions.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => {
                        setQuery(s);
                        setShowSuggestions(false);
                      }}
                      className="rounded bg-surface-container px-2.5 py-1 text-label-sm text-on-surface transition-colors hover:bg-surface-bright hover:text-primary"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Format tabs */}
        <div className="mb-space-lg flex items-center justify-between gap-space-md border-b border-surface-container-high">
          <div role="tablist" className="no-scrollbar flex items-center gap-space-lg overflow-x-auto">
            {resourceTabs.map((t) => (
              <button
                key={t.id}
                type="button"
                role="tab"
                aria-selected={type === t.id}
                onClick={() => setType(t.id)}
                className={`-mb-px shrink-0 border-b-2 pb-space-sm text-label-md transition-colors ${
                  type === t.id
                    ? "border-primary-container font-bold text-on-surface"
                    : "border-transparent text-on-surface-variant hover:text-on-surface"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
          <span className="hidden shrink-0 pb-space-sm text-label-sm text-secondary sm:inline-block" aria-live="polite">
            Showing {visible.length} resources
          </span>
        </div>

        {visible.length > 0 ? (
          <div className="grid grid-cols-1 gap-gutter md:grid-cols-2 lg:grid-cols-3">
            {visible.map((r) => {
              const s = typeStyle[r.type];
              return (
                <article
                  key={r.title}
                  className="group flex flex-col justify-between rounded-xl bg-surface-container-low p-space-md shadow-md transition-all hover:bg-surface-container"
                >
                  <div>
                    <div className="mb-space-xs flex items-center justify-between">
                      <span className={`flex items-center gap-1 rounded px-2 py-0.5 text-label-sm ${s.badge}`}>
                        <Icon name={s.icon} size={14} /> {r.format}
                      </span>
                      <span className="text-label-sm text-on-surface-variant">{r.kind}</span>
                    </div>
                    <h3 className="mt-2 font-display text-headline-sm text-on-surface transition-colors group-hover:text-primary">
                      {r.title}
                    </h3>
                    <p className="mt-1 text-body-sm text-on-surface-variant">{r.body}</p>
                  </div>
                  <div className="mt-space-md flex items-center justify-between border-t border-surface-container-high/50 pt-space-md">
                    <span className="text-label-sm text-secondary">{r.author}</span>
                    <a {...linkProps(r.href)} className="inline-flex items-center gap-1 text-label-sm font-bold text-primary hover:underline">
                      {s.cta} <Icon name={s.ctaIcon} size={16} />
                    </a>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="py-space-xl text-center">
            <Icon name="search_off" size={48} className="text-on-surface-variant" />
            <h3 className="mt-2 font-display text-headline-sm text-on-surface">No matching teachings or resources</h3>
            <p className="mt-1 text-body-sm text-on-surface-variant">Try another keyword or reset the filter tabs above.</p>
          </div>
        )}
      </Container>
    </section>
  );
}
