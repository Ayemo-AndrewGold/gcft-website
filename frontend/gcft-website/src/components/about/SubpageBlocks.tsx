/* Content blocks specific to individual About sub-pages. */
import { beliefPoints, messageScriptures, ministerProfiles } from "@/lib/about";
import { Container, Icon, linkProps } from "../ui";

/** Grid of outlined belief cards (Our Beliefs). */
export function BeliefGrid() {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="grid grid-cols-1 gap-gutter sm:grid-cols-2 lg:grid-cols-3">
          {beliefPoints.map((b, i) => {
            const inner = (
              <>
                <div className="mb-space-lg flex items-center justify-between">
                  <span className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary-container/10 text-primary-container">
                    <Icon name={b.icon} size={26} />
                  </span>
                  <span className="font-display text-[40px] leading-none text-white/10">{String(i + 1).padStart(2, "0")}</span>
                </div>
                <h3 className="font-body text-[22px] font-semibold text-on-surface transition-colors group-hover:text-primary-container">
                  {b.title}
                </h3>
                <p className="mt-space-xs text-body-md text-on-surface-variant">{b.body}</p>
                {b.href && (
                  <span className="mt-space-md inline-flex items-center gap-1 text-label-sm font-bold uppercase tracking-wider text-primary-container">
                    Read the teaching <Icon name="arrow_forward" size={14} />
                  </span>
                )}
              </>
            );
            const cls =
              "group block rounded-xl border border-white/15 p-space-lg transition-all duration-300 hover:-translate-y-1 hover:border-primary-container";
            return b.href ? (
              <a key={b.title} {...linkProps(b.href)} className={cls}>
                {inner}
              </a>
            ) : (
              <div key={b.title} className={cls}>
                {inner}
              </div>
            );
          })}
        </div>
      </Container>
    </section>
  );
}

/** Large scripture callouts (The Message). KJV text — public domain. */
export function ScriptureList() {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="grid grid-cols-1 gap-gutter lg:grid-cols-3">
          {messageScriptures.map((s) => (
            <figure
              key={s.ref}
              className="candle-glow flex flex-col justify-between rounded-xl border-l-2 border-primary-container bg-surface-container-low p-space-lg"
            >
              <blockquote className="font-display text-headline-sm italic leading-snug text-on-surface">“{s.text}”</blockquote>
              <figcaption className="mt-space-lg text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container">
                {s.ref} <span className="text-on-surface-variant">· KJV</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </Container>
    </section>
  );
}

/** Minister profile cards (Our Ministers). */
export function MinisterCards() {
  return (
    <section className="w-full bg-surface pb-section">
      <Container>
        <div className="grid grid-cols-1 gap-gutter md:grid-cols-2">
          {ministerProfiles.map((m) => (
            <article key={m.name} className="flex flex-col gap-space-lg rounded-xl border border-white/15 p-space-lg sm:flex-row md:p-space-xl">
              {/* Placeholder portrait — replace with a photo */}
              <div className="flex h-28 w-28 shrink-0 items-center justify-center rounded-xl bg-surface-container-high text-primary-container">
                <Icon name="person" size={56} />
              </div>
              <div className="min-w-0">
                <p className="text-[13px] font-bold uppercase tracking-[0.2em] text-primary-container">{m.role}</p>
                <h3 className="mt-1 font-display text-headline-md text-on-surface">{m.name}</h3>
                <p className="mt-space-sm text-body-md text-on-surface-variant">{m.body}</p>
                <div className="mt-space-md flex flex-wrap gap-space-sm">
                  {m.links.map((l) => (
                    <a
                      key={l.label}
                      {...linkProps(l.href)}
                      className="inline-flex items-center gap-1 rounded-lg border border-primary-container/45 px-space-md py-2 text-label-sm text-on-surface transition-colors hover:border-primary-container hover:bg-primary-container/10"
                    >
                      <Icon name={l.icon} size={16} className="text-primary-container" />
                      {l.label}
                    </a>
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>
      </Container>
    </section>
  );
}
