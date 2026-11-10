# 📊 SentimentIQ — Exploratory Data Analysis (EDA) Report

## 1. Overview & Provenance
- **Primary Benchmark Dataset**: `cardiffnlp/tweet_eval` (sentiment subset)
- **Total Samples Audited**: 59,865 samples
- **Splits**: Train (45,583), Validation (2,000), Test (12,282)

## 2. Split Composition & Class Balance

| Split | Negative Count (%) | Neutral Count (%) | Positive Count (%) | Total |
| :--- | :--- | :--- | :--- | :--- |
| **Train** | 7,091 (15.6%) | 20,653 (45.3%) | 17,839 (39.1%) | 45,583 |
| **Validation** | 312 (15.6%) | 869 (43.5%) | 819 (40.9%) | 2,000 |
| **Test** | 3,971 (32.3%) | 5,936 (48.3%) | 2,375 (19.3%) | 12,282 |

> [!NOTE]
> **Class Imbalance Observation**: In the training split, `negative` samples constitute ~15.6% of the dataset, whereas `neutral` and `positive` comprise ~45.3% and ~39.1% respectively. Consequently, **Macro F1-score** is strictly mandated as the primary evaluation metric (Section 8) to penalize models that neglect minority negative expressions.

## 3. Sequence Length Characteristics

| Metric | Train Words | Train Chars | Validation Words | Test Words |
| :--- | :--- | :--- | :--- | :--- |
| **Mean** | 19.24 | 106.52 | 19.44 | 14.86 |
| **Median** | 20.0 | 112.0 | 20.0 | 15.0 |
| **95th Percentile** | 27.0 | 140.0 | 27.0 | 24.0 |
| **Max** | 35 | 200 | 31 | 32 |

## 4. Top Vocabulary Signals per Sentiment Class

- **Negative**: `not` (2093), `may` (1567), `but` (906), `tomorrow` (881), `just` (790), `was` (753), `u002c` (691), `will` (656), `like` (590), `all` (528), `about` (523), `can` (499)
- **Neutral**: `may` (2895), `tomorrow` (2663), `not` (2612), `will` (2346), `u002c` (2235), `but` (1688), `just` (1628), `was` (1506), `from` (1339), `out` (1315), `going` (1296), `day` (1246)
- **Positive**: `tomorrow` (3094), `may` (2199), `not` (1951), `will` (1857), `day` (1820), `see` (1554), `u002c` (1529), `just` (1511), `was` (1357), `can` (1355), `all` (1331), `but` (1310)

## 5. Artifacts Generated
- `ml/artifacts/eda/class_distribution.png`
- `ml/artifacts/eda/length_distribution.png`
