# Repository Line Counts

Best-effort size snapshot of the repositories managed under `~/repos`.

- Snapshot date: 2026-08-19
- Repository scope: current working trees of all 50 top-level Git repositories
- Counting unit: nonblank physical lines in tracked text files

## Rebuild

Run `python3 scripts/rebuild-repository-line-counts.py` from the `ahara` repository root.

## Totals

| Category | Nonblank LoC |
| --- | ---: |
| Source, configuration, and tracked data | 2,769,062 |
| Tests | 578,292 |
| Markdown documentation | 275,986 |
| **All included text** | **3,623,340** |

## Method

- Counts nonblank physical lines in files returned by `git ls-files`; comments remain in the count.
- Classifies tests from common path and filename patterns such as `test/`, `tests/`, `spec/`, `e2e/`, `*_test.*`, `*.test.*`, and `*.spec.*`.
- Counts `.md` and `.mdx` files only as Markdown documentation, even when they occur under a test path.
- Classifies other tracked text by extension or well-known filename. JSON, YAML, SVG, XML, Terraform, and similar formats are included, so this is broader than executable source code.
- Excludes the generated report itself, common dependency and build directories, lockfiles, minified files, source maps, snapshots, binary or unrecognized files, and individual files over 5 MB.
- The size rule excluded 3 recognized text files in this snapshot.

The source, test, and Markdown columns are mutually exclusive. The test classification is a path heuristic, so test fixtures stored under those paths count as tests.

## Per repository

| Repository | Source LoC by language | Test LoC by language | Markdown docs |
| --- | ---: | ---: | ---: |
| ableton-extensions | TypeScript 1,305, JSON 192, JavaScript 27, YAML 25 | TypeScript 876 | 425 |
| agents-of-glass | Python 34,435, TypeScript 5,096, CSS 3,137, Rust 2,315, SQL 698, Shell 290, Terraform 280, TOML 222, JavaScript 112, JSON 68, YAML 25, HTML 19, Make 16 | Python 9,094 | 7,836 |
| ahara | YAML 1,296, Python 1,183, Shell 68, TOML 48, SVG 6 | Python 211 | 2,540 |
| ahara-access | Rust 1,590, Terraform 151, SQL 132, TOML 61, YAML 25, Shell 21, Make 19 | — | 111 |
| ahara-business | Rust 17,501, TypeScript 8,260, CSS 1,730, Terraform 747, SQL 556, JavaScript 148, TOML 142, JSON 105, Shell 63, SVG 44, YAML 32, HTML 27, Make 23 | Rust 3,036, TypeScript 2,512, JSON 78 | 1,045 |
| ahara-collector | Rust 5,070, Nix 1,842, Shell 201, JSON 54, YAML 33, TOML 19, Make 12 | Nix 602 | 1,115 |
| ahara-infra | Rust 9,205, Terraform 7,852, TOML 304, SQL 184, Shell 46, YAML 34, Make 23 | Rust 946 | 343 |
| ahara-observability | JSON 2,975, YAML 839, TypeScript 482, Shell 81, JavaScript 42, Dockerfile 33, Make 23 | TypeScript 54 | 325 |
| ahara-portal | TypeScript 4,137, CSS 3,537, JSON 839, JavaScript 214, Terraform 116, YAML 24, Shell 16, HTML 15, Make 8, SVG 4 | — | 312 |
| ahara-standards | JavaScript 734, JSON 445, TOML 7 | — | 1,966 |
| ahara-support-services | — | — | 0 |
| ahara-tf-patterns | Terraform 1,534 | — | 113 |
| ahara-trust | Nix 2,338, Rust 1,183, HTML 416, Shell 228, JSON 41, YAML 33, Make 14, TOML 13 | Nix 773 | 1,184 |
| ahara-vpn | Nix 3,595, Rust 1,048, Terraform 636, Shell 514, JSON 497, YAML 40, Make 18, TOML 16 | Nix 1,117 | 1,759 |
| airwave | Rust 8,766, TypeScript 6,187, Kotlin 849, XML 388, CSS 200, JSON 136, JavaScript 99, Terraform 97, YAML 97, TOML 69, Config 34, Dockerfile 32, Make 27, HTML 19, Properties 5, SVG 1 | TypeScript 1,644, Rust 688 | 574 |
| athena-s3-web-shell | TypeScript 14,010, CSS 4,279, Terraform 1,374, JavaScript 289, JSON 211, Shell 134, Dockerfile 58, HTML 42, Make 25, SVG 5, YAML 2 | TypeScript 4,049, JSON 31 | 1,059 |
| bookmarker | Rust 7,775, TypeScript 5,708, CSS 2,035, Kotlin 1,346, PowerShell 418, JavaScript 374, Shell 359, Terraform 312, SQL 296, JSON 105, TOML 103, XML 98, Make 92, SVG 63, HTML 45, YAML 27, Properties 9 | Rust 3,883, TypeScript 2,578 | 2,285 |
| catalyst-castellum | TypeScript 56,126, JSON 17,071, SVG 8,595, CSS 7,802, Ruby 1,432, Python 150, JavaScript 119, Terraform 70, Shell 56, HTML 45, YAML 34, Make 31 | TypeScript 8,023 | 2,561 |
| dosekit | TypeScript 2,247, Rust 1,674, CSS 1,040, SQL 487, JavaScript 392, Terraform 97, JSON 94, Shell 68, Make 32, TOML 29, HTML 26, YAML 25, SVG 16 | TypeScript 356 | 705 |
| etudes | — | — | 0 |
| foundry-modules | TypeScript 1,934, YAML 121, JSON 94, JavaScript 93, CSS 22, Make 13 | TypeScript 534 | 405 |
| foundry-vtt | Terraform 524, Rust 289, TOML 27, YAML 23, Shell 18, Make 15 | — | 483 |
| harbor | Python 29,231, TypeScript 9,595, CSS 1,483, JSON 469, YAML 321, Shell 149, JavaScript 89, Make 88, Terraform 75, Config 67, Dockerfile 57, TOML 38, INI 32, HTML 13 | Python 16,774, TypeScript 2,737, JSON 511 | 4,335 |
| hot-mic | C# 72,570, JSON 865, YAML 192, Make 10 | C# 3,754, Python 210, JSON 201 | 3,200 |
| house-sensors | Python 3,465, JSON 1,700, HTML 372, YAML 351, Dockerfile 155, Terraform 151, Make 23, TOML 11, Shell 5 | Python 732 | 444 |
| illuminator | TypeScript 3,180, Python 1,681, JSON 70, TOML 68, Shell 44, YAML 23 | JavaScript 729 | 722 |
| kontakt-shell | — | — | 4 |
| legato | Rust 20,322, Shell 287, TOML 251, Protocol Buffers 197, YAML 145, SQL 126, PowerShell 107, Dockerfile 17, Make 12 | Rust 707 | 1,821 |
| lindelion | Rust 114,669, SVG 32,769, TOML 1,431, TypeScript 820, CSS 356, Make 338, Python 258, Shell 61, YAML 52, JSON 46, HTML 12 | Rust 18,008 | 8,332 |
| nas-csi | Rust 17,283, YAML 707, Protocol Buffers 222, TOML 174, Python 109, Shell 39 | — | 2,880 |
| nas-falkordb | YAML 46, Make 9 | — | 61 |
| nas-text-embeddings-inference | YAML 55, Make 9 | — | 74 |
| oig-cdo | JSON 33,412, Python 7,178, JavaScript 1,368, Terraform 624, Shell 245, Make 53, YAML 36, Dockerfile 35, HTML 12 | — | 58,871 |
| opm-clarity | Ruby 38,377, JSON 10,495, JavaScript 1,795, CSS 639, Make 202, YAML 77, HTML 15, SVG 6 | Ruby 5,013, JavaScript 382 | 16,518 |
| scriptorium | TypeScript 8,929, JSON 50 | JavaScript 318, TOML 38 | 708 |
| scuba-sense | TypeScript 57,759, HTML 42,239, SQL 7,934, SVG 1,940, TOML 1,137, CSS 877, YAML 781, Shell 520, JSON 323, Make 277, JavaScript 129 | TypeScript 14,206, SQL 2,956 | 27,231 |
| sigillum | Python 171,045, Ruby 12,362, JSON 213, TOML 19 | Python 251 | 24,783 |
| sigillum-explorations | Ruby 14,073, JSON 991, TOML 18 | — | 13,269 |
| sigillum-library | Ruby 34,285, JSON 9,555, YAML 60 | JSON 387,210, Ruby 6,310 | 11,781 |
| sigillum-ml | Python 19,014, JSON 1,901, TypeScript 767, CSS 222, JavaScript 59, Ruby 40, TOML 22, HTML 12 | Python 3,991, TypeScript 83, Ruby 48 | 2,969 |
| slipstream | C# 12,051, YAML 176, JSON 4 | C# 899 | 898 |
| stax-infrastructure | YAML 9,325, Terraform 3,707, Shell 210, Dockerfile 40, Make 34, SVG 1 | — | 503 |
| sulion | Rust 47,065, TypeScript 21,022, CSS 7,269, SQL 1,637, Shell 1,262, JSON 1,210, JavaScript 1,151, Nix 892, Dockerfile 796, YAML 493, Terraform 210, TOML 104, Config 80, Python 70, Make 63, HTML 14, SVG 11 | Rust 9,393, TypeScript 8,627, Nix 201 | 5,265 |
| svap | JSON 36,438, Rust 7,855, TypeScript 3,739, CSS 1,485, SQL 813, JavaScript 602, Terraform 396, YAML 185, Shell 94, TOML 80, Make 42, HTML 16 | — | 4,347 |
| tastebase | TypeScript 5,843, Rust 5,536, CSS 3,333, Terraform 281, SQL 239, TOML 164, JavaScript 116, JSON 101, HTML 59, Shell 38, YAML 30, Make 22, SVG 4 | — | 206 |
| the-canonry | JSON 693,114, TypeScript 226,613, JavaScript 46,947, CSS 38,787, Python 1,211, Terraform 973, YAML 239, HTML 235, Shell 173, SVG 99, Properties 14 | JSON 1,884 | 18,149 |
| the-canonry-game | C# 138,518, JSON 137,433, Python 1,072, TOML 782, Make 181, Shell 25 | C# 30,926 | 16,993 |
| the-glass-frontier | JSON 97,540, TypeScript 31,376, CSS 5,573, JavaScript 3,938, Terraform 1,913, Shell 190, YAML 41, HTML 15 | TypeScript 1,038, JSON 839 | 13,848 |
| tsonu-canon | Ruby 15,310, TypeScript 1,934, CSS 1,531, JavaScript 780, Rust 279, Terraform 176, JSON 103, YAML 69, Make 64, HTML 36, TOML 30, SVG 19 | Ruby 2,504, TypeScript 157, JavaScript 36 | 5,016 |
| tsonu-music | TypeScript 38,554, Rust 7,881, CSS 4,177, Terraform 1,174, JSON 941, JavaScript 389, TOML 367, SQL 327, HTML 184, Shell 162, Make 37, YAML 29, XML 20 | TypeScript 14,653, Rust 881 | 5,612 |

## Language summary

Markdown is omitted here because it is reported separately.

| Language | Source | Tests | Combined |
| --- | ---: | ---: | ---: |
| JSON | 1,049,901 | 390,754 | 1,440,655 |
| TypeScript | 515,623 | 62,127 | 577,750 |
| Rust | 277,306 | 37,542 | 314,848 |
| Python | 270,102 | 31,263 | 301,365 |
| C# | 223,139 | 35,579 | 258,718 |
| Ruby | 115,879 | 13,875 | 129,754 |
| CSS | 89,514 | 0 | 89,514 |
| JavaScript | 60,006 | 1,465 | 61,471 |
| HTML | 43,888 | 0 | 43,888 |
| SVG | 43,583 | 0 | 43,583 |
| Terraform | 23,470 | 0 | 23,470 |
| SQL | 13,429 | 2,956 | 16,385 |
| YAML | 16,168 | 0 | 16,168 |
| Nix | 8,667 | 2,693 | 11,360 |
| TOML | 5,756 | 38 | 5,794 |
| Shell | 5,667 | 0 | 5,667 |
| Kotlin | 2,195 | 0 | 2,195 |
| Make | 1,855 | 0 | 1,855 |
| Dockerfile | 1,223 | 0 | 1,223 |
| PowerShell | 525 | 0 | 525 |
| XML | 506 | 0 | 506 |
| Protocol Buffers | 419 | 0 | 419 |
| Config | 181 | 0 | 181 |
| INI | 32 | 0 | 32 |
| Properties | 28 | 0 | 28 |
| **Total** | **2,769,062** | **578,292** | **3,347,354** |

## Markdown documentation by repository

Repositories with no Markdown are omitted from this table but remain present in the per-repository table.

| Repository | Markdown LoC | Markdown files |
| --- | ---: | ---: |
| oig-cdo | 58,871 | 766 |
| scuba-sense | 27,231 | 185 |
| sigillum | 24,783 | 166 |
| the-canonry | 18,149 | 141 |
| the-canonry-game | 16,993 | 241 |
| opm-clarity | 16,518 | 188 |
| the-glass-frontier | 13,848 | 245 |
| sigillum-explorations | 13,269 | 98 |
| sigillum-library | 11,781 | 97 |
| lindelion | 8,332 | 126 |
| agents-of-glass | 7,836 | 149 |
| tsonu-music | 5,612 | 50 |
| sulion | 5,265 | 38 |
| tsonu-canon | 5,016 | 36 |
| svap | 4,347 | 47 |
| harbor | 4,335 | 70 |
| hot-mic | 3,200 | 38 |
| sigillum-ml | 2,969 | 35 |
| nas-csi | 2,880 | 56 |
| catalyst-castellum | 2,561 | 39 |
| ahara | 2,540 | 21 |
| bookmarker | 2,285 | 32 |
| ahara-standards | 1,966 | 43 |
| legato | 1,821 | 17 |
| ahara-vpn | 1,759 | 34 |
| ahara-trust | 1,184 | 15 |
| ahara-collector | 1,115 | 27 |
| athena-s3-web-shell | 1,059 | 13 |
| ahara-business | 1,045 | 26 |
| slipstream | 898 | 6 |
| illuminator | 722 | 10 |
| scriptorium | 708 | 20 |
| dosekit | 705 | 6 |
| airwave | 574 | 7 |
| stax-infrastructure | 503 | 3 |
| foundry-vtt | 483 | 15 |
| house-sensors | 444 | 14 |
| ableton-extensions | 425 | 9 |
| foundry-modules | 405 | 13 |
| ahara-infra | 343 | 6 |
| ahara-observability | 325 | 5 |
| ahara-portal | 312 | 10 |
| tastebase | 206 | 4 |
| ahara-tf-patterns | 113 | 3 |
| ahara-access | 111 | 9 |
| nas-text-embeddings-inference | 74 | 3 |
| nas-falkordb | 61 | 3 |
| kontakt-shell | 4 | 2 |
| **Total** | **275,986** | **3,187** |
