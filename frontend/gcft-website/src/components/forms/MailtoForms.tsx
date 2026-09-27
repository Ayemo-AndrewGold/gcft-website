"use client";

/*
 * Until a backend endpoint exists, these forms compose an email to the church
 * inbox in the visitor's mail app (mailto:). Swap `send()` for a fetch() to
 * your API when the backend is ready.
 */
import { useState, type FormEvent } from "react";
import { site } from "@/lib/content";
import { enquiryTopics } from "@/lib/pages";
import { Icon } from "../ui";

const inputCls =
  "w-full rounded-lg border border-on-surface/15 bg-surface-container-lowest/60 px-space-md py-3 text-body-md text-on-surface placeholder:text-[#8e95a5] transition-colors focus:border-primary-container focus:ring-1 focus:ring-primary-container/35 focus:outline-none";
const labelCls = "mb-1.5 block text-label-sm uppercase tracking-wider text-on-surface-variant";

function send(subject: string, body: string) {
  window.location.href = `mailto:${site.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

export function EnquiryForm() {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const get = (k: string) => String(f.get(k) ?? "").trim();
    if (get("email") !== get("confirm")) {
      setError("Email addresses do not match.");
      return;
    }
    setError("");
    send(
      `[Website] ${get("topic")} — ${get("first")} ${get("last")}`,
      `Name: ${get("first")} ${get("last")}\nEmail: ${get("email")}\nTopic: ${get("topic")}\n\n${get("message")}`,
    );
    setSent(true);
  };

  return (
    <form onSubmit={onSubmit} className="grid grid-cols-1 gap-space-md sm:grid-cols-2">
      <div className="sm:col-span-2">
        <label htmlFor="topic" className={labelCls}>
          Subject
        </label>
        <select id="topic" name="topic" className={inputCls} defaultValue={enquiryTopics[0]}>
          {enquiryTopics.map((t) => (
            <option key={t} value={t} className="bg-surface">
              {t}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="first" className={labelCls}>
          First Name
        </label>
        <input id="first" name="first" required autoComplete="given-name" className={inputCls} placeholder="First name" />
      </div>
      <div>
        <label htmlFor="last" className={labelCls}>
          Last Name
        </label>
        <input id="last" name="last" required autoComplete="family-name" className={inputCls} placeholder="Last name" />
      </div>
      <div>
        <label htmlFor="email" className={labelCls}>
          Email
        </label>
        <input id="email" name="email" type="email" required autoComplete="email" className={inputCls} placeholder="you@example.com" />
      </div>
      <div>
        <label htmlFor="confirm" className={labelCls}>
          Confirm Email
        </label>
        <input id="confirm" name="confirm" type="email" required className={inputCls} placeholder="Confirm email" />
      </div>
      <div className="sm:col-span-2">
        <label htmlFor="message" className={labelCls}>
          Message
        </label>
        <textarea id="message" name="message" required rows={6} className={`${inputCls} resize-y`} placeholder="How can we help?" />
      </div>
      <div className="flex flex-col gap-space-sm sm:col-span-2 sm:flex-row sm:items-center sm:justify-between">
        <p role="status" className={`text-body-sm ${error ? "text-error" : "text-on-surface-variant"}`}>
          {error || (sent ? "Your email app should now be open with your message. Thank you!" : `Messages go to ${site.email}.`)}
        </p>
        <button
          type="submit"
          className="inline-flex shrink-0 items-center justify-center gap-space-xs rounded-lg bg-primary-container px-space-xl py-3 text-label-md uppercase tracking-wider text-on-primary shadow-glow transition-all hover:bg-primary-fixed"
        >
          Send Message <Icon name="send" size={18} />
        </button>
      </div>
    </form>
  );
}

export function NewsletterSignup({ cta = "Subscribe", compact = false }: { cta?: string; compact?: boolean }) {
  const [sent, setSent] = useState(false);

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const name = String(f.get("name") ?? "").trim();
    const email = String(f.get("email") ?? "").trim();
    send("Subscribe me to GCFT Weekly", `Please add me to the GCFT Weekly newsletter.\n\nName: ${name}\nEmail: ${email}`);
    setSent(true);
  };

  return (
    <form onSubmit={onSubmit} className="w-full">
      <div className={`flex flex-col gap-space-sm ${compact ? "sm:flex-row" : "md:flex-row"}`}>
        {!compact && (
          <input name="name" required autoComplete="name" aria-label="Your name" placeholder="Your name" className={inputCls} />
        )}
        <input name="email" type="email" required autoComplete="email" aria-label="Email address" placeholder="Email address" className={inputCls} />
        <button
          type="submit"
          className="inline-flex shrink-0 items-center justify-center gap-space-xs rounded-lg bg-primary-container px-space-xl py-3 text-label-md uppercase tracking-wider text-on-primary shadow-glow transition-all hover:bg-primary-fixed"
        >
          {cta} <Icon name="arrow_forward" size={18} />
        </button>
      </div>
      {sent && (
        <p role="status" className="mt-space-sm flex items-center gap-space-xs text-body-sm text-primary">
          <Icon name="check_circle" size={18} /> Your email app is open — just press send to confirm your subscription.
        </p>
      )}
    </form>
  );
}
