# Material bindings

## Source policy

Shared AI conversations are useful discovery material, not authoritative answer
keys. Claims about an exam question must ultimately bind to the original PDF page
or another authoritative source. Every extracted item should preserve source,
year, page, transcription status, and any discrepancy.

## Currently bound materials

| ID | Material | Observed scope | Present status | Permitted use |
| --- | --- | --- | --- | --- |
| DS-SOLID | [DeepSeek solid-state share](https://chat.deepseek.com/share/fwg1jg8yli1zztblqc) | 196-message discussion organized around solid-state exam preparation | Full public conversation text is accessible; one PDF attachment is listed but its bytes and pages are not yet locally verified | Candidate problems, interpretations, corrections, and leads only |
| DS-617 | [DeepSeek 617 share](https://chat.deepseek.com/share/9efwi337sjl26meu3k) | 190-message discussion organized around USTC 617 general-physics preparation | Full public conversation text is accessible; two PDF attachments are listed but their bytes and pages are not yet locally verified | Candidate problems, interpretations, corrections, and leads only |
| A617-LOCAL | [Local A617 compilation](</H:/Storage/Affair/普通物理/中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf>) | 36-page compilation containing 2010–2025 papers despite inconsistent cover/preface labels | File hashed; all pages text-readable; representative 2023–2025 pages visually checked; detailed audit in [sources/a617-local-corpus.md](sources/a617-local-corpus.md) | Page-bound problem statements and independent derivations, but not official marking guidance |

Observed attachment names:

- DS-SOLID: `中国科学院大学硕士研究生试题.pdf`;
- DS-617: `中国科学技术大学普通物理历年考研真题及答案.pdf`;
- DS-617: `中国科学技术大学研究生入学考试习题汇编—普通物理A617.pdf`.

The first filename and the conversation's claimed institutional scope may not
match. This is a provenance question for M0, not something to silently normalize.

### Public-access boundary observed during source recovery

The public share endpoint returns conversation text and attachment metadata,
including opaque file identifiers. A direct unauthenticated request for a listed
identifier at the file-fetch endpoint returned application code `40003` with
`INVALID_TOKEN`. No attachment bytes or stable public download URL were exposed by
the two share records.

Consequently, cases drawn only from the two DeepSeek shares remain provisionally
bound to transcript wording. They are not promoted as page-verified exam questions,
and no attachment checksum or visual-page validation is claimed for them. This
restriction does not apply to the separately bound `A617-LOCAL` artifact.

## Required corpus record

Each original problem should eventually produce a record with:

```text
ProblemSource {
  corpus_id,
  institution,
  exam_or_course,
  year,
  problem_number,
  page,
  source_file,
  source_checksum,
  transcription,
  diagrams,
  answer_source,
  correction_log,
  confidence
}
```

## Reliability ladder

1. original examination scan;
2. official solution or marking guidance;
3. independently checked derivation;
4. published textbook or primary reference for theorem contracts;
5. third-party solution compilation;
6. shared-chat explanation.

Lower levels may discover a question or interpretation. They may not override a
higher-level source without an explicit contradiction record.

## Immediate material gap

The A617 compilation is now locally bound and selected newer problems have exact
page references. The remaining gaps are an official provenance/answer source and
the separate solid-state attachment. Claims based only on the shared conversations
remain provisional.
