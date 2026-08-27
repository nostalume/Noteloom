# Notes

This repository is a collection of notes and documents (kernel experiments, physics notes, Typst sources, and small utilities). Some content is published to [`nexus`](https://nostalume.github.io/Nexus-Blog); the `kernel/` section is commonly posted.

## Layout

- `physics/` — all physics content: markdown notes, Typst sources, theses, and topic subdirectories (`am/`, `em/`, `et/`, `qm/`, etc.). Shared entry point at `physics/lib.typ` reexports the Typst template from `manus/`.
- `kernel/` — OS/kernel notes and experiments (`arceos/`, `ipc/`, `rcore/`). Many subfolders are mounted into the Hugo site.
- `sketches/` — teaching materials, physics sketches, and miscellaneous notes.
- `manus/` — git submodule providing shared Typst templates and utilities.

### Physics subdirectories

Multi-file topics get their own subdirectory; single-file topics live flat in `physics/`.

| Path | Topic |
|------|-------|
| `physics/am/` | Classical mechanics (Typst, mindmaps) |
| `physics/em/` | Electromagnetism (Typst) |
| `physics/em-*.md` | Electromagnetism (markdown notes) |
| `physics/et/` | Electronics (Typst, images) |
| `physics/et-*.md` | Electronics (markdown notes) |
| `physics/qm/` | Quantum mechanics (3 Typst files) |
| `physics/sm/` | State machines |
| `physics/am-thesis/` | Lie groups & Galilean invariance thesis |
| `physics/cp-thesis/` | Computational physics methods thesis |
| `physics/cat/` | Category theory & homology |
| `physics/dg/` | Differential geometry |
| `physics/sr.md` | Special relativity |

## How the site is assembled

This project uses Hugo with module mounts configured in `config.toml`. Top-level folders (for example `kernel/arceos/axembassy` and `kernel/ipc`) are mounted into the site via `[[module.mounts]]` entries. Do not expect an editable `content/` directory — edit the top-level source folders instead.

Example mount (in `config.toml`):

```toml
[[module.mounts]]
source = "kernel/ipc"
target = "content/posts/nostalgia"
```

To add a new post that appears on the site:

- Create your post under a top-level folder, e.g. `kernel/new-topic/my-post.md`.
- Add or update a `[[module.mounts]]` entry in `config.toml` mapping the source folder (or file) to a `content/` target the site expects.
- Run a local preview with `hugo server -D`.

## Templates and Typst

- Typst templates live under `manus/` (submodule). The local entry point `physics/lib.typ` reexports `manus/mine.typ`.
- To compile a Typst document locally:

```bash
typst compile physics/<path>/main.typ
```

If you want to add a Hugo template or layout, add files under the theme or `layouts/` used by Hugo. Keep templates small and reference them in posts with front matter when needed.

## Developer workflows

- Local preview (requires Hugo installed):

```bash
hugo server -D
hugo --minify    # build static site
```

- Go toolchain: a `go.mod` exists at the project root; some tools or modules may require a Go toolchain (`go 1.25.1` specified).
