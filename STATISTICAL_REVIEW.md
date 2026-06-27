# pyqicharts Statistical Review

Status: v1.2.1 specification-complete, validation-enhanced parity candidate.

This review compares the implementation against published methodology descriptions and SPC reference formulae, not live R/qicharts2 output.

## References

- Anhøj J, Olesen AV. Run charts revisited: a simulation study of run chart rules for detection of non-random variation in health care processes. PLOS ONE, 2014.
- Anhøj J, Wentzel-Larsen T. Sense and sensibility: on the diagnostic value of control chart rules for detection of shifts in time series data. BMC Medical Research Methodology, 2018.
- Nelson LS. The Shewhart Control Chart: Tests for Special Causes. Journal of Quality Technology, 1984.
- Western Electric Company. Statistical Quality Control Handbook, 1956.
- NIST/SEMATECH e-Handbook of Statistical Methods, section on Shewhart X-bar, R and S charts.
- Montgomery DC. Introduction to Statistical Quality Control.
- NHS Making Data Count statistical process control guidance.

Useful public summaries consulted:

- Nelson rule descriptions: https://en.wikipedia.org/wiki/Nelson_rules
- Western Electric zone rules: https://en.wikipedia.org/wiki/Western_Electric_rules
- Xbar/S formulas and constants: https://en.wikipedia.org/wiki/X%CC%85_and_s_chart
- Xbar/R constant table summary: https://en.wikipedia.org/wiki/X%CC%85_and_R_chart

## Anhøj Run Charts

Formula used:

- Centre line is the median of non-missing, non-excluded observations.
- Values equal to the median are omitted from the run/crossing sequence.
- Runs are consecutive observations on the same side of the median.
- Crossings are side changes in the median-excluded sign sequence.
- Long-run threshold uses the Schilling-style logarithmic critical length `ceil(log2(n) + 3)` for `n >= 10`.
- Few-crossing threshold uses the exact lower tail of `Binomial(n - 1, 0.5)`.

Implementation notes:

- Missing values are dropped.
- Excluded observations are removed from calculations.
- Short series return deterministic non-signal summaries.

Known deviations:

- No live qicharts2 output comparison is bundled.

## bestbox and cutbox

Formula used:

- `bestbox` searches deterministic observed and midpoint centre candidates and chooses the centre with the strongest non-signal margin.
- `cutbox` trims one low and one high observation when at least five observations exist, then performs the same centre-candidate search.

Implementation notes:

- qicharts2 documents these methods as experimental. Published descriptions do not provide a single universally normative closed-form formula, so pyqicharts uses a deterministic, documented candidate-search equivalent.

Known deviations:

- This is specification-based, not byte-for-byte R certification.

## Nelson Rules 1-8

Formula used:

- Rule 1: one point beyond 3 sigma.
- Rule 2: nine points on the same side of centre.
- Rule 3: six points increasing or decreasing.
- Rule 4: fourteen alternating increases/decreases.
- Rule 5: two of three beyond 2 sigma on same side.
- Rule 6: four of five beyond 1 sigma on same side.
- Rule 7: fifteen within 1 sigma.
- Rule 8: eight outside 1 sigma with both sides represented.

Implementation notes:

- Centre and sigma can be scalar or per-point series.
- Missing values and non-positive sigma values are ignored safely.
- Segment-aware tables pass segment-specific centre and sigma values.

## Shewhart Rules

Formula used:

- Rule S1: point outside 3 sigma limits.
- S2/S3/S4/S5 are mapped to Western Electric/Nelson-style zone, run and trend checks.

Known deviations:

- Full Western Electric asymmetric-zone adaptations for skewed charts are not separately implemented; chart-specific limits are used for primary breach detection.

## Xbar and S Charts

Formula used:

- Xbar centre: weighted grand mean of subgroup means.
- Xbar limits: centre ± 3 * sigma / sqrt(n_i).
- S centre: average subgroup standard deviation.
- S limits: B3/B4-style normal-theory limits derived from `c4(n_i)`.

Implementation notes:

- Variable subgroup sizes use subgroup-specific limits.
- Baseline, break/recalculation, exclusions and phases are supported.

## P-prime and U-prime

Formula used:

- P-prime with denominator: risk-adjusted proportion, plotting O/E scaled by the segment observed proportion.
- U-prime with denominator: risk-adjusted rate, plotting O/E scaled by the segment observed rate.
- Without denominators, both are explicitly labelled observed/expected fallback charts.

Known deviations:

- Case-mix model fitting is outside package scope; expected values are supplied by the user.

## G and T Charts

Formula used:

- G chart assumes geometric rare-event intervals with probability `p = 1 / (mean + 1)`.
- T chart assumes exponential waiting times.
- Limits use 0.00135/0.99865 tail probabilities as 3-sigma-equivalent rare-event tails.

Implementation notes:

- Negative intervals are invalid.
- Zero intervals are accepted and handled.
- Segments use segment-specific means and limits.
