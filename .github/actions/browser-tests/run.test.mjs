import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { run, runtime } from "./run.mjs";

function fixture(t, version = "1.63.0", dependency = "playwright") {
  const root = mkdtempSync(join(tmpdir(), "ahara-browser-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const frontend = join(root, "apps/web");
  const installed =
    dependency === "playwright"
      ? join(frontend, "node_modules/playwright")
      : join(frontend, "node_modules/@playwright/test/node_modules/playwright");
  mkdirSync(installed, { recursive: true });
  writeFileSync(join(frontend, "package.json"), "{}");
  writeFileSync(join(installed, "package.json"), JSON.stringify({ version }));
  if (dependency !== "playwright") {
    writeFileSync(
      join(frontend, "node_modules/@playwright/test/package.json"),
      "{}",
    );
  }
  return root;
}

test("browser image follows installed Playwright, including pnpm's nested test dependency", (t) => {
  for (const dependency of ["playwright", "@playwright/test"]) {
    const root = fixture(t, "1.62.1", dependency);
    const args = runtime(root, "apps/web", "webkit", "image");
    assert.ok(args.includes("PLAYWRIGHT_VERSION=1.62.1"));
    assert.ok(args.includes("ahara-browser-tests:1.62.1"));
  }
});

test("container uses the declared engine and script with automatic cleanup and caller ownership", (t) => {
  const root = fixture(t);
  const args = runtime(root, "apps/web", "firefox", "test:release");
  assert.deepEqual(args.slice(-4), [
    "ahara-browser-tests:1.63.0",
    "pnpm",
    "run",
    "test:release",
  ]);
  assert.ok(args.includes("BROWSER=firefox"));
  assert.ok(args.includes("/workspace/apps/web"));
  assert.ok(args.includes("--rm"));
  assert.ok(args.includes(`${process.getuid()}:${process.getgid()}`));
  assert.ok(args.includes(`type=bind,src=${root},dst=/workspace`));
});

test("test failure and interrupted container execution remain failures", (t) => {
  const root = fixture(t);
  assert.equal(
    run(root, "apps/web", "chromium", "test:browser", () => ({ status: 17 })),
    17,
  );
  assert.equal(
    run(root, "apps/web", "chromium", "test:browser", () => ({
      status: null,
      signal: "SIGTERM",
    })),
    1,
  );
  assert.throws(
    () =>
      run(root, "apps/web", "chromium", "image", () => ({
        error: new Error("docker unavailable"),
      })),
    /docker unavailable/,
  );
});

test("invalid engines, scripts, checkout paths and image versions fail before execution", (t) => {
  const root = fixture(t);
  for (const [directory, engine, script] of [
    ["../other", "chromium", "image"],
    ["/tmp", "chromium", "image"],
    ["apps/web", "chrome", "image"],
    ["apps/web", "chromium", "arbitrary"],
  ])
    assert.throws(() => runtime(root, directory, engine, script));
  const prerelease = fixture(t, "1.64.0-next");
  assert.throws(
    () => runtime(prerelease, "apps/web", "chromium", "image"),
    /stable version/,
  );
});
