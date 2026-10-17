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
    const { args } = runtime(root, "apps/web", "webkit", "setup");
    assert.ok(args.includes("PLAYWRIGHT_VERSION=1.62.1"));
    assert.ok(args.includes("ahara-browser-tests:1.62.1-pnpm-10.29.3"));
  }
});

test("container uses the declared engine and script with automatic cleanup and caller ownership", (t) => {
  const root = fixture(t);
  const { args } = runtime(root, "apps/web", "firefox", "test:release");
  assert.deepEqual(args.slice(-4), [
    "ahara-browser-tests:1.63.0-pnpm-10.29.3",
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
    run(root, "apps/web", "chromium", "test:browser", "container", () => ({
      status: 17,
    })),
    17,
  );
  assert.equal(
    run(root, "apps/web", "chromium", "test:browser", "container", () => ({
      status: null,
      signal: "SIGTERM",
    })),
    1,
  );
  assert.throws(
    () =>
      run(root, "apps/web", "chromium", "setup", "container", () => ({
        error: new Error("docker unavailable"),
      })),
    /docker unavailable/,
  );
});

test("invalid engines, scripts, checkout paths and image versions fail before execution", (t) => {
  const root = fixture(t);
  for (const [directory, engine, script] of [
    ["../other", "chromium", "setup"],
    ["/tmp", "chromium", "setup"],
    ["apps/web", "chrome", "setup"],
    ["apps/web", "chromium", "arbitrary"],
  ])
    assert.throws(() => runtime(root, directory, engine, script));
  const prerelease = fixture(t, "1.64.0-next");
  assert.throws(
    () => runtime(prerelease, "apps/web", "chromium", "setup"),
    /stable version/,
  );
});

test("container package manager follows the selected package or its workspace root", (t) => {
  const root = fixture(t);
  writeFileSync(
    join(root, "package.json"),
    JSON.stringify({ packageManager: "pnpm@10.23.0" }),
  );
  assert.ok(
    runtime(root, "apps/web", "chromium", "setup").args.includes(
      "PNPM_VERSION=10.23.0",
    ),
  );
  writeFileSync(
    join(root, "apps/web/package.json"),
    JSON.stringify({ packageManager: "pnpm@10.33.0" }),
  );
  assert.ok(
    runtime(root, "apps/web", "chromium", "setup").args.includes(
      "PNPM_VERSION=10.33.0",
    ),
  );
});

test("explicit host runtime preserves Docker-backed harnesses and installs only the selected engine", (t) => {
  const root = fixture(t);
  assert.deepEqual(runtime(root, "apps/web", "chromium", "setup", "host"), {
    command: "pnpm",
    cwd: join(root, "apps/web"),
    args: ["exec", "playwright", "install", "--with-deps", "chromium"],
  });
  assert.deepEqual(
    runtime(root, "apps/web", "chromium", "test:browser", "host"),
    {
      command: "pnpm",
      cwd: join(root, "apps/web"),
      args: ["run", "test:browser"],
    },
  );
  let selected;
  assert.equal(
    run(
      root,
      "apps/web",
      "firefox",
      "test:browser",
      "host",
      (command, args, options) => {
        selected = {
          command,
          args,
          cwd: options.cwd,
          browser: options.env.BROWSER,
          ci: options.env.CI,
        };
        return { status: 9 };
      },
    ),
    9,
  );
  assert.deepEqual(selected, {
    command: "pnpm",
    args: ["run", "test:browser"],
    cwd: join(root, "apps/web"),
    browser: "firefox",
    ci: "1",
  });
  assert.throws(
    () => runtime(root, "apps/web", "chromium", "setup", "invalid"),
    /Unsupported browser runtime/,
  );
});
