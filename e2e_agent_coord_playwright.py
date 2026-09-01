#!/usr/bin/env python3
"""Playwright check for nav, shared aside, and agent-coord cross-links.

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
    assert "Atlanta / Remote" in text
    assert "todd.espy@gmail.com" in text
    assert "linkedin.com/in/toddespy" in text


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
            assert page.locator(".site-nav a").count() == 6
            assert page.locator('a[href*="agent-coord.html"]').count() == 0
            assert page.locator('a[href="/#agent-coord"]').count() == 0
            assert "github.com/t-espy/agent-coord" not in page.content()
            assert page.locator("#agent-coord").count() == 0
            _assert_contact(page)
            assert page.locator(".credentials-sidebar").is_visible()
            assert "MSEE, Duke University" in page.locator(
                ".credentials-sidebar"
            ).inner_text()
            page.screenshot(path=str(SHOTS / "home-card.png"), full_page=True)

            page.locator('a[href="methodology.html#agent-coord-board"]').click()
            page.wait_for_url("**/methodology.html#agent-coord-board")
            board = page.locator("#agent-coord-board")
            board.wait_for()
            assert "fourth place is a coordination board" in board.inner_text()
            _assert_contact(page)
            related = page.locator("#contact h2", has_text="Related")
            assert related.count() == 1
            page.screenshot(path=str(SHOTS / "methodology-jump.png"), full_page=True)

            page.locator('#agent-coord-board a[href="lean-optimizer.html"]').click()
            page.wait_for_url("**/lean-optimizer.html")
            assert page.locator('a[href="/#agent-coord"]').count() == 0
            _assert_contact(page)

            page.goto(f"{base}/autonomous-improvement-rate.html", wait_until="domcontentloaded")
            _assert_contact(page)
            assert page.locator('#contact a[href="/autonomous-improvement-rate-technical.html"]').count() == 1
            assert page.locator(".credentials-sidebar").count() == 0
            assert page.locator('a[href="/#agent-coord"]').count() == 0

            page.goto(f"{base}/qwen38-dgx-spark.html", wait_until="domcontentloaded")
            _assert_contact(page)
            assert page.locator('#contact a[href="/autonomous-improvement-rate.html"]').count() == 1

            page.goto(
                f"{base}/technical-credentials.html", wait_until="domcontentloaded"
            )
            assert page.locator("#contact").count() == 0

            phone = browser.new_page(viewport={"width": 390, "height": 844})
            phone.goto(f"{base}/", wait_until="domcontentloaded")
            assert phone.locator(".site-nav a").count() == 6
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
