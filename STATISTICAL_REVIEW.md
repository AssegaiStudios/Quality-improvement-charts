# pyqicharts Statistical Review

Status: v1.3.4 specification-complete, validation-enhanced parity candidate.

This review verifies pyqicharts against published methodology descriptions and standard SPC formulae. It does not claim byte-for-byte certification against live R `qicharts`, live R `qicharts2` or NHS workbook outputs.

## Reference Base

- Anhøj J, Olesen AV. Run charts revisited: a simulation study of run chart rules for detection of non-random variation in health care processes. PLoS ONE, 2014.
- Anhøj J. Diagnostic value of run chart analysis: using likelihood ratios to compare run chart rules on simulated data series. PLoS ONE, 2015.
- Nelson LS. The Shewhart Control Chart: Tests for Special Causes. Journal of Quality Technology, 1984.
- Western Electric Company. Statistical Quality Control Handbook, 1956.
- Montgomery DC. Introduction to Statistical Quality Control.
- NIST/SEMATECH e-Handbook of Statistical Methods.
- NHS England / Making Data Count SPC guidance.

Public reference summaries also consulted:

- https://en.wikipedia.org/wiki/Control_chart
- https://en.wikipedia.org/wiki/Nelson_rules
- https://en.wikipedia.org/wiki/C-chart
- https://en.wikipedia.org/wiki/P-chart
- https://en.wikipedia.org/wiki/U-chart
- https://en.wikipedia.org/wiki/X%CC%85_and_s_chart
- https://en.wikipedia.org/wiki/X%CC%85_and_R_chart

## Anhøj Run Charts

Formula verified:

- Centre line is the median of eligible observations.
- Observations equal to the median are removed before counting runs or crossings.
- A run is a consecutive sequence on one side of the median.
- A crossing is a side change in the median-excluded sequence.
- Few-crossings threshold uses an exact lower tail of `Binomial(n - 1, 0.5)`.
- Longest-run threshold uses the commonly cited logarithmic Schilling-style rule `ceil(log2(n) + 3)` for larger `n`.

Implementation notes:

- Missing values are dropped.
- Excluded rows are removed from the centre and signal source.
- Segment-specific run chart calculations are performed after break/recalculation metadata is applied.

Known deviations:

- Exact published lookup tables are not bundled as independent validation artifacts.

## bestbox and cutbox

Formula verified:

- `bestbox` evaluates deterministic observed and midpoint centre candidates.
- Each candidate is scored by how far it remains from triggering a run-chart signal.
- The best-scoring candidate is used as the centre.
- `cutbox` trims one low and one high observation for series with at least five observations, then applies the same deterministic centre search.

Implementation notes:

- These methods are exposed through `method="bestbox"` and `method="cutbox"`.
- They are deterministic and tested for stable output.

Known deviations:

- qicharts2 describes these methods as experimental; no single closed-form published standard was identified. pyqicharts therefore documents its candidate-search implementation.

## Nelson Rules 1-8

Formula verified:

- N1: one point more than 3 sigma from centre.
- N2: nine consecutive points on the same side of centre.
- N3: six consecutive increasing or decreasing points.
- N4: fourteen consecutive alternating up/down points.
- N5: two of three consecutive points beyond 2 sigma on the same side.
- N6: four of five consecutive points beyond 1 sigma on the same side.
- N7: fifteen consecutive points within 1 sigma of centre.
- N8: eight consecutive points outside 1 sigma, with both sides represented.

Implementation notes:

- Centre and sigma may be scalar or per-point series.
- Segment-aware tables call the rule engine separately per segment.
- Missing and non-positive sigma values safely produce no rule output.

Known deviations:

- The rules are emitted as metadata; they do not replace chart-specific primary signal logic.

## Shewhart Rules

Formula verified:

- Primary Shewhart detection is the 3-sigma point-beyond-limits rule.
- For charts with direct control limits, points outside LCL/UCL are flagged.
- The `shewhart_rule_signals(...)` helper returns a stable signal-schema DataFrame.

Implementation notes:

- In `qic_table(...)`, chart-specific limits are authoritative.
- The helper is mainly for explicit rule-table workflows.

Known deviations:

- Full Western Electric zone-rule families are not independently exposed beyond the Nelson-compatible structure.

## Individuals and Moving Range Charts

Formula verified:

```text
Individuals centre = mean(x)
MR_i = abs(x_i - x_(i-1))
MRbar = mean(MR_i)
sigma = MRbar / 1.128
I LCL/UCL = centre +/- 3 * sigma
MR centre = MRbar
MR LCL = 0
MR UCL = 3.267 * MRbar
```

Implementation notes:

- Baseline/freeze uses the first eligible segment source.
- Breaks/recalculation create independent segment means and limits.
- Excluded rows are visible but do not contribute to source calculations or signal outputs.

Known deviations:

- The moving-range constant assumes adjacent moving ranges of size 2, matching the intended XmR use case.

## C, P and U Charts

Formula verified:

```text
C chart:
cbar = mean(c)
LCL = max(0, cbar - 3 * sqrt(cbar))
UCL = cbar + 3 * sqrt(cbar)

P chart:
p_i = events_i / n_i
pbar = sum(events) / sum(n)
SE_i = sqrt(pbar * (1 - pbar) / n_i)
LCL_i = max(0, pbar - 3 * SE_i)
UCL_i = min(1, pbar + 3 * SE_i)

U chart:
u_i = events_i / n_i
ubar = sum(events) / sum(n)
SE_i = sqrt(ubar / n_i)
LCL_i = max(0, ubar - 3 * SE_i)
UCL_i = ubar + 3 * SE_i
```

Implementation notes:

- P and U charts require positive denominators.
- Segment-specific centres and limits are calculated independently.

Known deviations:

- No overdispersion adjustment is currently applied.

## Xbar and S Charts

Formula verified:

```text
xbar_i = subgroup mean
s_i = subgroup sample standard deviation
grand mean = weighted mean of subgroup means
sbar = mean(s_i)
c4(n) = sqrt(2 / (n - 1)) * gamma(n / 2) / gamma((n - 1) / 2)
sigma = sbar / c4(nbar)
Xbar limits = grand mean +/- 3 * sigma / sqrt(n_i)
S limits = sbar * (1 +/- 3 * sqrt(1 - c4(n_i)^2) / c4(n_i))
```

Implementation notes:

- Variable subgroup sizes receive point-specific limits.
- Excluded subgroups are removed from centre/limit calculations and signal text is cleared.

Known deviations:

- The implementation uses calculated normal-theory constants rather than fixed printed A3/B3/B4 tables.

## P-prime and U-prime Charts

Formula verified:

```text
OE_i = observed_i / expected_i
denominator-aware centre = sum(observed) / sum(denominator)
plot_i = OE_i * centre

P-prime SE_i = centre * sqrt((1 - expected_probability_i) / (expected_probability_i * denominator_i))
U-prime SE_i = centre / sqrt(expected_i)

fallback centre = 1
fallback SE_i = 1 / sqrt(expected_i)
```

Implementation notes:

- P-prime proportion logic and U-prime rate logic are separate.
- Zero expected values are converted to missing adjusted ratios/limits rather than causing division errors.
- Negative expected values raise `ValueError`.

Known deviations:

- pyqicharts does not fit risk models; users supply expected values.

## G and T Charts

Formula verified:

```text
G:
p = 1 / (mean interval + 1)
LCL = max(0, log(0.99865) / log(1 - p) - 1)
UCL = max(0, log(0.00135) / log(1 - p) - 1)

T:
LCL = -mean interval * log(0.99865)
UCL = -mean interval * log(0.00135)
```

Implementation notes:

- Inputs must be non-negative intervals already prepared by the user.
- Zero intervals are allowed.
- v1.3.4 adds dedicated segmented G/T fixtures with stored expected outputs.

Known deviations:

- Tail probabilities are 3-sigma-equivalent approximations; no exact healthcare workbook reference output is bundled.

## Segment-Aware Validation

Verified behaviour:

- Segment 1, segment 2 and segment 3 use their own centre lines and limits.
- Freeze points work independently of break/recalculation points.
- Breaks, recalculation points, phases and exclusions are carried through output tables.
- Excluded rows clear Boolean and text signal fields.

## Overall Conclusion

The implementation is consistent with published SPC formulas and documented healthcare QI practice for the supported chart families. The remaining evidence limitation is external certification: deterministic internal validation fixtures are bundled, but live cross-package and published-workbook comparisons are not.
