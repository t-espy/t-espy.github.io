#!/usr/bin/env python3
"""Playwright check for nav, shared aside, and current portfolio cross-links.

Serves this directory. Uses lean-optimizer's Playwright (not a site dependency).

  /home/tespy/lean-optimizer/venv/bin/python e2e_agent_coord_playwright.py
"""
from __future__ import annotations

import http.server
import socket
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "_playwright_shots"


def _serve() -> tuple[threading.Thread, int, http.server.HTTPServer]:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def log_message(self, fmt, *args):  # noqa: ARG002
            return

    httpd = http.server.HTTPServer(("127.0.0.1", port), Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return t, port, httpd


def _assert_contact(page) -> None:
    aside = page.locator("#contact")
    aside.wait_for()
    text = aside.inner_text()
    assert "Remote / Atlanta-area hybrid" in text
    assert "todd.espy@gmail.com" in text
    assert "linkedin.com/in/toddespy" in text


def _assert_nav(page) -> None:
    nav = page.locator(".site-nav a")
    assert nav.count() == 5
    assert nav.all_text_contents() == [
        "Home",
        "Work",
        "AI Engineering",
        "Writing",
        "Credentials",
    ]


def main() -> int:
    from playwright.sync_api import sync_playwright

    SHOTS.mkdir(exist_ok=True)
    _, port, httpd = _serve()
    base = f"http://127.0.0.1:{port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})

            page.goto(f"{base}/", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator(".credentials-sidebar").is_visible()
            assert "MSEE, Duke University" in page.locator(
                ".credentials-sidebar"
            ).inner_text()
            assert page.locator('a[href="ratchetloop.html"]').count() >= 1
            assert page.locator('a[href="asset-factory.html"]').count() >= 1
            assert page.locator('a[href="work.html"]').count() >= 1
            assert page.locator('a[href="writing.html"]').count() >= 1
            assert page.locator('a[href="2026-output.html"]').count() >= 1
            page.screenshot(path=str(SHOTS / "home-card.png"), full_page=True)

            page.goto(f"{base}/work.html", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator('a[href="ratchetloop.html"]').count() >= 1
            assert page.locator(
                'a[href="https://github.com/t-espy/leetcode-python"]'
            ).count() >= 1
            assert page.locator('a[href="2026-output.html"]').count() >= 1
            assert page.locator('a[href="asset-factory.html"]').count() >= 1

            page.goto(f"{base}/asset-factory.html", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator("h1").inner_text() == "Asset Factory"
            assert page.locator('.site-nav a[aria-current="page"]').inner_text() == "Work"
            assert "Assets Forge is one brand and output channel" in page.locator("main").inner_text()
            assert page.locator(".media-placeholder").count() == 9
            assert page.locator('a[href="https://assetsforge.net"]').count() >= 1

            page.goto(f"{base}/2026-output.html", wait_until="domcontentloaded")
            _assert_nav(page)
            assert page.locator("h1").inner_text() == "2026 Engineering Output"
            assert page.locator('.site-nav a[aria-current="page"]').inner_text() == "Work"
            assert "Lines of code are not a measure" in page.locator("main").inner_text()

            page.goto(f"{base}/ratchetloop.html", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator(
                'a[href="https://github.com/t-espy/ratchetloop-public"]'
            ).count() >= 1
            assert page.locator(
                'a[href="https://github.com/t-espy/leetcode-python"]'
            ).count() >= 1

            page.goto(
                f"{base}/methodology.html#delivery-control-loop",
                wait_until="domcontentloaded",
            )
            _assert_nav(page)
            _assert_contact(page)
            loop = page.locator("#delivery-control-loop")
            loop.wait_for()
            assert "Ratchetloop" in loop.inner_text()
            assert "durable record" in loop.inner_text()
            assert page.locator("#contact h2", has_text="Related").count() == 1
            page.screenshot(path=str(SHOTS / "methodology-jump.png"), full_page=True)

            page.goto(f"{base}/lean-optimizer.html", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator('a[href="ratchetloop.html"]').count() >= 1

            page.goto(
                f"{base}/autonomous-improvement-rate.html",
                wait_until="domcontentloaded",
            )
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator(
                '#contact a[href="/autonomous-improvement-rate-technical.html"]'
            ).count() == 1
            assert page.locator(".credentials-sidebar").count() == 0

            page.goto(f"{base}/qwen38-dgx-spark.html", wait_until="domcontentloaded")
            _assert_nav(page)
            _assert_contact(page)
            assert page.locator('#contact a[href="/writing.html"]').count() == 1
            assert page.locator('#contact a[href="/ratchetloop.html"]').count() == 1

            page.goto(f"{base}/technical-credentials.html", wait_until="domcontentloaded")
            _assert_nav(page)
            assert page.locator("#contact").count() == 0

            phone = browser.new_page(viewport={"width": 390, "height": 844})
            phone.goto(f"{base}/", wait_until="domcontentloaded")
            _assert_nav(phone)
            _assert_contact(phone)
            phone.screenshot(path=str(SHOTS / "home-card-mobile.png"), full_page=True)
            phone.close()
            browser.close()
    finally:
        httpd.shutdown()
    print("PASS")
    print(f"shots: {SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
