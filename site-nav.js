const SITE_NAV_LINKS = [
  {
    href: "/",
    label: "Home",
    current: (file) => file === "" || file === "index.html",
  },
  {
    href: "/work.html",
    label: "Work",
    current: (file) =>
      ["work.html", "ratchetloop.html", "asset-factory.html", "meetup-finder.html", "lean-optimizer.html", "2026-output.html"].includes(file),
  },
  {
    href: "/methodology.html",
    label: "AI Engineering",
    current: (file) => file === "methodology.html",
  },
  {
    href: "/writing.html",
    label: "Writing",
    current: (file) =>
      ["writing.html", "autonomous-improvement-rate.html", "autonomous-improvement-rate-technical.html",
       "qwen38-dgx-spark.html"].includes(file),
  },
  {
    href: "/technical-credentials.html",
    label: "Credentials",
    current: (file) => file === "technical-credentials.html",
  },
];

function currentFile() {
  const file = location.pathname.split("/").pop();
  return file ?? "";
}

class SiteNav extends HTMLElement {
  connectedCallback() {
    const file = currentFile();
    const nav = document.createElement("nav");
    nav.className = "site-nav";
    nav.setAttribute("aria-label", "Site");

    for (const link of SITE_NAV_LINKS) {
      const anchor = document.createElement("a");
      anchor.href = link.href;
      anchor.textContent = link.label;
      if (link.current(file)) {
        anchor.setAttribute("aria-current", "page");
      }
      nav.appendChild(anchor);
    }

    this.replaceWith(nav);
  }
}

customElements.define("site-nav", SiteNav);
