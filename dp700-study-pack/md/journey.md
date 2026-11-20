# From 619 to 745: how I passed DP-700 on the second try

My first DP-700 attempt scored **619**, which was 81 points short of the 700 pass mark. On **Nov 17, 2026** I passed with **745**. This is what changed between the two attempts.

## Where I started

I've worked in data engineering for over 15 years, mostly T-SQL, SQL Server, SSIS and Azure Data Factory, and more recently Microsoft Fabric and PySpark. Day-to-day experience helped less than I expected. The exam rewards knowing exact product behaviour: limits, defaults, who is allowed to do what, and which feature is the documented fix. After the first attempt, my weak areas were **security and governance, streaming, and error resolution**.

I rescheduled the retake from Oct 26 to Nov 17 to give myself time to prepare properly.

## The plan

**1. Build one source of truth from Microsoft Learn (Oct 11).**
With Claude as a study partner, I built a Reading Pack that maps every bullet of the official skills outline to the Microsoft Learn pages behind it. Every fact had to come from a Learn page, with the link. Anything the docs don't say directly was marked "Unverified."
While building it, I found eight claims in my own earlier notes that current docs contradict. Fabric changes quickly, so check old notes and blog posts against Learn.

**2. Make it easy to review.**
I turned the pack into a short two-host audio walk-through (seven episodes, about 78 minutes) so I could review on walks.

**3. Measure honestly (Nov 7).**
Microsoft's practice assessment gave me 72%, against my target of 80%. It confirmed that monitoring, optimization and error resolution were my weakest domain.

**4. Practice with hard scenario questions (Nov 6–16).**
Claude wrote exam-style scenario questions with several constraints each, with the answers hidden until I committed. Grading always explained every option, not only the correct one. Every miss went into the Reading Pack straight away, and facts I missed twice went on a short "repeat-miss" list.

| Date | Practice set | Score |
| --- | --- | --- |
| Nov 6 | Mixed questions 1–5 | 4 / 5 |
| Nov 7 | Case study | 3 / 5 |
| Nov 7 | Microsoft practice assessment | 72% |
| Nov 12 | Ingest and transform (16 questions) | 11 / 16 |
| Nov 12–13 | Monitor and optimize (two sets of 10) | 7 / 10, 6 / 10 |
| Nov 13–15 | Implement and manage (two sets of 10) | 4 / 10, 6 / 10 |
| Nov 15 | Full mock 1 (45 questions) | 34 / 45 |
| Nov 16 | Full mock 2 (45 questions, mostly new topics) | 41 / 45 |
| Nov 16 | Full mock 3 (45 questions, choose-two and Yes/No formats) | 34 / 45 |

**5. Stop the night before.**
After mock 3, I reviewed only the misses and went to bed. On exam morning I spent 20 minutes on the repeat-miss list and nothing else.

## Result

**745 / 1000, PASS.** Implement and manage was my strongest section. Monitor and optimize is still my shortest bar, so that's where I'll keep learning.

## What worked

- **Docs first, with links.** If I couldn't point to the Learn sentence, I didn't treat it as a fact.
- **Explain every option.** Knowing why three answers are wrong is what lets you handle a new scenario.
- **A repeat-miss list.** Most misses were exceptions to a general rule. Those are what to reread on exam morning.
- **Hard practice formats.** Choose-two and Yes/No sets with all-or-nothing scoring showed gaps that single-answer questions hid.
- **Trusting my first instinct.** Twice in the mocks I changed a correct first answer to a wrong one. When two options both seemed plausible, my first pick was usually the better one.
- **Using AI as a study partner, not as an answer source.** Claude wrote questions, graded them and explained the reasoning. The facts always came from Microsoft Learn, and I checked them there.

## The materials

Everything I studied from is in this pack: the [reading pack](reading-pack.html), the [question bank](question-bank.html) and three full mocks with answer keys ([Mock 1](mock-1.html), [Mock 2](mock-2.html), [Mock 3](mock-3.html)). None of it comes from the real exam. It was all written from public Microsoft Learn documentation.

Good luck. If this helps you pass, I'd love to hear about it.
