# DP-700 Fabric Study Pack

Free study materials for **DP-700: Implementing Data Engineering Solutions Using Microsoft Fabric** (Microsoft Certified: Fabric Data Engineer Associate).

I'm Ankur Jain, a senior data engineer. I failed DP-700 the first time with 619 (the pass mark is 700). I rebuilt my preparation from scratch, and on **Nov 17, 2026 I passed with 745**. These are the materials I studied from, cleaned up so anyone can use them. The full story is in [journey.md](journey.md).

## What's inside

| File | What it is |
| --- | --- |
| [reading-pack.md](reading-pack.md) | A 14-part study guide that covers every skill in the DP-700 outline, grouped by exam domain. It includes tables, code patterns, hands-on labs and a list of common traps (Part 14). Every part links its Microsoft Learn sources. |
| [question-bank.md](question-bank.md) | 66 scenario questions with hidden answers and a one-line reason for each. |
| [mocks/](mocks/) | Three full 45-question mock exams, each with a separate answer key. Mock 3 uses choose-two and Yes/No formats with all-or-nothing scoring. |
| [journey.md](journey.md) | How I went from 619 to 745: the plan, the scores along the way, and what I'd do again. |

## How to use it

1. Read the [official DP-700 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700) first, because it's the source of truth for what's measured.
2. Work through the Reading Pack one domain at a time, and do the matching lab after each part.
3. Use the question bank to find your weak spots. Read the explanation for every option, not only the right one.
4. Take the mocks under time (100 minutes, no notes), then review every miss against the Reading Pack.
5. Before the exam, reread Part 14 (common traps) and your own list of facts you've missed more than once.

Microsoft's own practice assessment, linked from the [certification page](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/), is worth taking as well.

## How it was made

I built these with **Claude (Anthropic) as my study coach**. The rules were strict:
- Every fact had to come from a Microsoft Learn page opened that day, with a link.
- Any point Learn doesn't state directly is marked **Unverified**, and no answer depends on it alone.
- Every question was graded answer-first, with an explanation for each option.
- Every miss went into the Reading Pack so it couldn't be missed twice.

## Please read

- **No real exam content.** All questions were written from public documentation before I sat the exam, and every scenario is fictional. This folder will never include recalled exam questions; the [Microsoft exam agreement](https://learn.microsoft.com/en-us/certifications/microsoft-exam-agreement) prohibits sharing them, and please don't post any in issues.
- **Not affiliated with Microsoft.** This is a personal study resource, not official material.
- **Fabric changes fast.** Facts were checked between Oct 11 and Nov 16, 2026. If a detail matters, open the linked Learn page. Corrections are welcome as issues or pull requests; please include the Learn link.

## License and attribution

My content in this folder is © 2026 Ankur Jain, licensed under [CC BY 4.0](LICENSE). The license covers this folder only. You can share and adapt it as long as you give credit.

The materials quote and summarize [Microsoft Learn](https://learn.microsoft.com/) documentation, which Microsoft publishes under CC BY 4.0 (see the [fabric-docs repository](https://github.com/MicrosoftDocs/fabric-docs)). Sources are linked throughout. Microsoft, Microsoft Fabric and related names are trademarks of Microsoft Corporation.
