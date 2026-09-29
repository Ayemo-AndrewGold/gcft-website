/*
 * Shared primitives for the v2 landing page.
 * Design language: hairline rules, mono indices, large tight display type,
 * a single precise accent. Server-safe (no hooks) except where noted.
 */
import Link from "next/link";
import type { ReactNode } from "react";
import { Icon, linkProps } from "../ui";

/** Numbered section header: "01 — Label" on a hairline, then the title. */
export function SectionHead({
  index,
  label,
  title,
  aside,
  className = "",
}: {
  index: string;
  label: string;
  title?: ReactNode;
  aside?: ReactNode;
  className?: string;
}) {
  return (
    <header className={`border-t border-hairline pt-6 ${className}`}>
      <div className="flex items-center justify-between gap-6">
        <p className="eyebrow flex items-center gap-3 text-on-surface-variant">
          <span className="text-primary-container">{index}</span>
          <span aria-hidden="true" className="h-px w-6 bg-hairline-strong" />
          <span>{label}</span>
        </p>
        {aside}
      </div>
      {title && (
        <h2 className="mt-10 max-w-4xl text-[34px] leading-[1.05] font-medium tracking-[-0.035em] text-on-surface md:mt-14 md:text-[56px]">
          {title}
        </h2>
      )}
    </header>
  );
}

/** Serif italic accent inside display headings. */
export function Accent({ children }: { children: ReactNode }) {
  return <em className="font-serif font-light tracking-[-0.02em] italic">{children}</em>;
}

/** Text link with a sliding arrow. Internal paths use next/link. */
export function ArrowLink({
  href,
  children,
  className = "",
  external,
}: {
  href: string;
  children: ReactNode;
  className?: string;
  external?: boolean;
}) {
  const cls = `group inline-flex items-center gap-2 text-label-md text-on-surface transition-colors hover:text-primary-container ${className}`;
  const inner = (
    <>
      <span className="relative">
        {children}
        <span className="absolute -bottom-0.5 left-0 h-px w-full origin-left scale-x-0 bg-current transition-transform duration-500 ease-out-expo group-hover:scale-x-100" />
      </span>
      <Icon
        name={external ? "arrow_outward" : "arrow_forward"}
        size={16}
        className="transition-transform duration-500 ease-out-expo group-hover:translate-x-0.5"
      />
    </>
  );
  const isInternal = href.startsWith("/") && !external;
  return isInternal ? (
    <Link href={href} className={cls}>
      {inner}
    </Link>
  ) : (
    <a {...linkProps(href)} className={cls}>
      {inner}
    </a>
  );
}

/** Pill buttons. `primary` = accent fill; `ghost` = hairline outline. */
export function Button({
  href,
  children,
  variant = "primary",
  icon,
  className = "",
}: {
  href: string;
  children: ReactNode;
  variant?: "primary" | "ghost" | "light";
  icon?: ReactNode;
  className?: string;
}) {
  const styles = {
    primary: "bg-primary-container text-on-primary hover:bg-primary-fixed",
    light: "bg-on-surface text-surface hover:bg-white",
    ghost: "border border-hairline-strong text-on-surface hover:border-white/40 hover:bg-white/[0.04]",
  }[variant];
  const cls = `inline-flex h-12 items-center justify-center gap-2.5 rounded-full px-6 text-[15px] font-medium tracking-[-0.01em] transition-colors duration-300 ${styles} ${className}`;
  const content = (
    <>
      {icon}
      {children}
    </>
  );
  return href.startsWith("/") ? (
    <Link href={href} className={cls}>
      {content}
    </Link>
  ) : (
    <a {...linkProps(href)} className={cls}>
      {content}
    </a>
  );
}

/** Pulsing live indicator dot. */
export function LiveDot({ className = "" }: { className?: string }) {
  return (
    <span className={`relative inline-flex h-2 w-2 ${className}`} aria-hidden="true">
      <span className="absolute inset-0 animate-ping rounded-full bg-error opacity-60" />
      <span className="relative inline-flex h-2 w-2 rounded-full bg-error" />
    </span>
  );
}
