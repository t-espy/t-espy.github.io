function currentFile() {
  const file = location.pathname.split("/").pop();
  return file ?? "";
}

const SITE_ASIDE = {
  "": { home: true },
  "index.html": { home: true },
  "work.html": {
    related: [
      { href: "/ratchetloop.html", label: "Ratchetloop" },
      { href: "/lean-optimizer.html", label: "Strategy Assayer" },
      { href: "/asset-factory.html", label: "Asset Factory" },
      { href: "/meetup-finder.html", label: "Meetup Finder" },
    ],
  },
  "asset-factory.html": {
    related: [
      { href: "/work.html", label: "Work portfolio" },
      { href: "/qwen38-dgx-spark.html", label: "Local model engineering" },
      {
        href: "https://assetsforge.net",
        label: "Assets Forge",
        external: true,
      },
    ],
  },
  "ratchetloop.html": {
    related: [
      {
        href: "https://github.com/t-espy/ratchetloop-public",
        label: "ratchetloop-public",
        external: true,
      },
      {
        href: "https://github.com/t-espy/leetcode-python",
        label: "leetcode-python work sample",
        external: true,
      },
      { href: "/methodology.html", label: "AI Engineering methodology" },
    ],
  },
  "meetup-finder.html": {
    related: [
      { href: "/work.html", label: "Work portfolio" },
      { href: "/methodology.html", label: "AI Engineering methodology" },
      {
        href: "https://meetupfinder.com",
        label: "Meetup Finder beta",
        external: true,
      },
    ],
  },
  "lean-optimizer.html": {
    related: [
      { href: "/work.html", label: "Work portfolio" },
      {
        href: "https://github.com/t-espy/lean-optimizer-public",
        label: "lean-optimizer-public",
        external: true,
      },
      { href: "/methodology.html", label: "AI Engineering methodology" },
    ],
  },
  "methodology.html": {
    related: [
      { href: "/ratchetloop.html", label: "Ratchetloop" },
      { href: "/work.html", label: "Work portfolio" },
      { href: "/autonomous-improvement-rate.html", label: "Autonomous Improvement Rate" },
    ],
  },
  "writing.html": {
    related: [
      { href: "/methodology.html", label: "AI Engineering methodology" },
      { href: "/work.html", label: "Work portfolio" },
    ],
  },
  "autonomous-improvement-rate.html": {
    related: [
      { href: "/writing.html", label: "Writing" },
      {
        href: "/autonomous-improvement-rate-technical.html",
        label: "Technical notes",
      },
      { href: "/ratchetloop.html", label: "Ratchetloop" },
      { href: "/lean-optimizer.html", label: "Strategy Assayer" },
    ],
  },
  "autonomous-improvement-rate-technical.html": {
    related: [
      { href: "/writing.html", label: "Writing" },
      {
        href: "/autonomous-improvement-rate.html",
        label: "Autonomous Improvement Rate",
      },
    ],
  },
  "qwen38-dgx-spark.html": {
    related: [
      { href: "/writing.html", label: "Writing" },
      {
        href: "https://github.com/t-espy/langgraph-factory",
        label: "langgraph-factory",
        external: true,
      },
      { href: "/ratchetloop.html", label: "Ratchetloop" },
    ],
  },
};

function linkEl(item) {
  const anchor = document.createElement("a");
  anchor.href = item.href;
  anchor.textContent = item.label;
  if (item.external) {
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
  }
  return anchor;
}

function listItem(label, content) {
  const li = document.createElement("li");
  const strong = document.createElement("strong");
  strong.textContent = `${label}:`;
  li.append(strong, " ", content);
  return li;
}

function fillEmail(root) {
  const slot = root.querySelector("#email");
  if (!slot) return;
  const address = "todd.espy@gmail.com";
  const mail = document.createElement("a");
  mail.href = `mailto:${address}`;
  mail.textContent = address;
  slot.replaceWith(mail);
}

class SiteAside extends HTMLElement {
  connectedCallback() {
    const file = currentFile();
    const config = SITE_ASIDE[file] ?? {};
    const aside = document.createElement("aside");
    aside.className = config.home ? "sidebar contact-sidebar" : "sidebar";
    aside.id = "contact";

    const contactHeading = document.createElement("h2");
    contactHeading.textContent = "Contact";
    const contactList = document.createElement("ul");
    const emailSlot = document.createElement("span");
    emailSlot.id = "email";
    const linkedin = document.createElement("a");
    linkedin.href = "https://www.linkedin.com/in/toddespy/";
    linkedin.target = "_blank";
    linkedin.rel = "noopener noreferrer";
    linkedin.textContent = "linkedin.com/in/toddespy";
    contactList.append(
      listItem("Work model", document.createTextNode("Remote / Atlanta-area hybrid")),
      listItem("Email", emailSlot),
      listItem("LinkedIn", linkedin),
    );
    aside.append(contactHeading, contactList);

    if (config.related?.length) {
      const relatedHeading = document.createElement("h2");
      relatedHeading.textContent = "Related";
      const relatedList = document.createElement("ul");
      for (const item of config.related) {
        const li = document.createElement("li");
        li.appendChild(linkEl(item));
        relatedList.appendChild(li);
      }
      aside.append(relatedHeading, relatedList);
    }

    this.replaceWith(aside);
    fillEmail(aside);
  }
}

customElements.define("site-aside", SiteAside);
