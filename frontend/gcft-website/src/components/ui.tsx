import type { ReactNode } from "react";

/** Props for links that should open in a new tab when they leave the site. */
export function linkProps(href: string) {
  return /^https?:\/\//.test(href) ? { href, target: "_blank", rel: "noopener noreferrer" } : { href };
}

/** Material Symbols icon. `fill` renders the solid variant. */
export function Icon({
  name,
  size = 20,
  fill = false,
  className = "",
}: {
  name: string;
  size?: number;
  fill?: boolean;
  className?: string;
}) {
  return (
    <span
      aria-hidden="true"
      className={`material-symbols-outlined ${fill ? "icon-fill" : ""} ${className}`}
      style={{ fontSize: size }}
    >
      {name}
    </span>
  );
}

/** Max-width content container aligned to the 1320px shell. */
export function Container({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`mx-auto w-full max-w-shell px-margin-sm md:px-10 lg:px-margin ${className}`}>{children}</div>;
}

/** Uppercase overline used above section headlines. */
export function Eyebrow({
  children,
  variant = "rule",
  className = "",
}: {
  children: ReactNode;
  variant?: "rule" | "dot";
  className?: string;
}) {
  return (
    <div className={`inline-flex items-center gap-space-xs ${className}`}>
      {variant === "rule" ? (
        <span className="h-[2px] w-8 bg-primary" />
      ) : (
        <span className="h-2.5 w-2.5 rounded-full bg-primary-container" />
      )}
      <span className="font-body text-label-sm uppercase tracking-widest text-primary">{children}</span>
    </div>
  );
}

export function SectionTitle({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <h2 className={`font-display text-headline-lg-mobile text-on-surface md:text-headline-lg ${className}`}>
      {children}
    </h2>
  );
}

/** Background-image block that zooms slightly on parent `group` hover. */
export function CoverImage({ src, alt, className = "" }: { src: string; alt: string; className?: string }) {
  return (
    <div
      role="img"
      aria-label={alt}
      className={`h-full w-full bg-cover bg-center transition-transform duration-500 group-hover:scale-105 ${className}`}
      style={{ backgroundImage: `url('${src}')` }}
    />
  );
}

/** Round prev/next controls for horizontal carousels. */
export function CarouselControls({
  onPrev,
  onNext,
  label,
  small = false,
}: {
  onPrev: () => void;
  onNext: () => void;
  label: string;
  small?: boolean;
}) {
  const btn = `${small ? "h-8 w-8" : "h-9 w-9"} flex items-center justify-center rounded-full bg-surface-container text-on-surface transition-colors hover:bg-surface-container-high hover:text-primary`;
  return (
    <div className="flex items-center gap-space-xs">
      <button type="button" aria-label={`Previous ${label}`} className={btn} onClick={onPrev}>
        <Icon name={small ? "chevron_left" : "arrow_back"} size={small ? 16 : 18} />
      </button>
      <button type="button" aria-label={`Next ${label}`} className={btn} onClick={onNext}>
        <Icon name={small ? "chevron_right" : "arrow_forward"} size={small ? 16 : 18} />
      </button>
    </div>
  );
}
