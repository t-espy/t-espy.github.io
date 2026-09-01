const SITE_NAV_LINKS = [
  {
    href: "/",
    label: "Home",
    current: (file) => file === "" || file === "index.html",
  },
  {
    href: "/methodology.html",
    label: "AI Engineering Methodology",
    current: (file) => file === "methodology.html",
  },
  {
    href: "/autonomous-improvement-rate.html",
    label: "Autonomous Improvement Rate",
    current: (file) =>
      file === "autonomous-improvement-rate.html" ||
      file === "autonomous-improvement-rate-technical.html",
  },
  {
    href: "/meetup-finder.html",
    label: "Meetup Finder",
    current: (file) => file === "meetup-finder.html",
  },
  {
    href: "/lean-optimizer.html",
    label: "Strategy Assayer",
    current: (file) => file === "lean-optimizer.html",
  },
  {
    href: "/technical-credentials.html",
    label: "Technical Credentials",
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
