import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { isAbsolute, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

function packageManagerVersion(root, workdir) {
  for (const directory of new Set([workdir, root])) {
    let packageJson;
    try {
      packageJson = JSON.parse(
        readFileSync(resolve(directory, "package.json"), "utf8"),
      );
    } catch (error) {
      if (error.code === "ENOENT") continue;
      throw error;
    }
    if (!packageJson.packageManager) continue;
    const version = /^pnpm@(\d+\.\d+\.\d+)(?:\+.*)?$/.exec(
      packageJson.packageManager,
    )?.[1];
    if (!version)
      throw new Error(
        "Browser containers require an exact pnpm packageManager version",
      );
    return version;
  }
  return "10.29.3";
}

export function runtime(
  root,
  directory,
  engine,
  script,
  execution = "container",
) {
  const workdir = resolve(root, directory);
  const location = relative(root, workdir);
  if (
    isAbsolute(directory) ||
    location === ".." ||
    location.startsWith("../")
  ) {
    throw new Error("Browser directory must stay within the repository");
  }
  if (!["chromium", "firefox", "webkit"].includes(engine)) {
    throw new Error(`Unsupported browser engine: ${engine}`);
  }
  if (!["setup", "test:browser", "test:release"].includes(script)) {
    throw new Error(`Unsupported browser script: ${script}`);
  }
  if (!["container", "host"].includes(execution)) {
    throw new Error(`Unsupported browser runtime: ${execution}`);
  }
  if (execution === "host") {
    return {
      command: "pnpm",
      args:
        script === "setup"
          ? ["exec", "playwright", "install", "--with-deps", engine]
          : ["run", script],
      cwd: workdir,
    };
  }
  let require = createRequire(resolve(workdir, "package.json"));
  let version;
  try {
    version = require("playwright/package.json").version;
  } catch (error) {
    if (error.code !== "MODULE_NOT_FOUND") throw error;
    require = createRequire(require.resolve("@playwright/test/package.json"));
    version = require("playwright/package.json").version;
  }
  if (!/^\d+\.\d+\.\d+$/.test(version)) {
    throw new Error(
      `Playwright needs a stable version for its browser image: ${version}`,
    );
  }
  const pnpmVersion = packageManagerVersion(root, workdir);
  const image = `ahara-browser-tests:${version}-pnpm-${pnpmVersion}`;
  if (script === "setup") {
    return {
      command: "docker",
      cwd: root,
      args: [
        "build",
        "--build-arg",
        `PLAYWRIGHT_VERSION=${version}`,
        "--build-arg",
        `PNPM_VERSION=${pnpmVersion}`,
        "--tag",
        image,
        fileURLToPath(new URL(".", import.meta.url)),
      ],
    };
  }
  return {
    command: "docker",
    cwd: root,
    args: [
      "run",
      "--rm",
      "--init",
      "--ipc=host",
      "--user",
      `${process.getuid()}:${process.getgid()}`,
      "--mount",
      `type=bind,src=${root},dst=/workspace`,
      "--workdir",
      `/workspace/${location}`,
      "--env",
      "CI=1",
      "--env",
      `BROWSER=${engine}`,
      image,
      "pnpm",
      "run",
      script,
    ],
  };
}

export function run(
  root,
  directory,
  engine,
  script,
  execution = "container",
  spawn = spawnSync,
) {
  const invocation = runtime(root, directory, engine, script, execution);
  const result = spawn(invocation.command, invocation.args, {
    cwd: invocation.cwd,
    stdio: "inherit",
    env: { ...process.env, CI: "1", BROWSER: engine },
  });
  if (result.error) throw result.error;
  return result.status ?? 1;
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(resolve(process.argv[1])).href
) {
  process.exitCode = run(process.cwd(), ...process.argv.slice(2));
}
