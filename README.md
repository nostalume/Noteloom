# Noteloom

Noteloom contains current personal notes, Typst sources, and selected document
outputs. Content is organized by subject; Git history retains removed or obsolete
material.

Nexus owns Hugo rendering, validation, theme integration, and deployment. This
repository exposes only the entries explicitly admitted by `config.toml`.

## Writing and publication

- Keep Markdown focused on one subject with ordered headings and fenced code.
- Put images and attachments beside a published note and use relative links.
- A published PDF uses a page bundle whose front matter declares `type = "pdf"`
  and `document = "file.pdf"`.
- Treat generated PDFs as disposable unless they are explicitly selected for
  version control.
- Verify every Markdown or PDF publication through the Nexus contract and
  production build; Noteloom is not a standalone Hugo site.

## Typst

Reusable templates come from the pinned `manus` submodule. Clone with submodules
enabled, or initialize it after cloning:

```bash
git submodule update --init --recursive
```

Compile a document from the repository root, for example:

```bash
typst compile --root . physics/condensed.typ
```
