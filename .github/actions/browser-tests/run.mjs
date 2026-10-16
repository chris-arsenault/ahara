import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { isAbsolute, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export function runtime(root, directory, engine, script) {
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
  if (!["image", "test:browser", "test:release"].includes(script)) {
    throw new Error(`Unsupported browser script: ${script}`);
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
  const image = `ahara-browser-tests:${version}`;
  if (script === "image") {
    return [
      "build",
      "--build-arg",
      `PLAYWRIGHT_VERSION=${version}`,
      "--tag",
      image,
      fileURLToPath(new URL(".", import.meta.url)),
    ];
  }
  return [
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
  ];
}

export function run(root, directory, engine, script, spawn = spawnSync) {
  const result = spawn("docker", runtime(root, directory, engine, script), {
    stdio: "inherit",
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
