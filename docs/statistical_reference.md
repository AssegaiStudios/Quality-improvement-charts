# Statistical Reference

This page records the formulas implemented by pyqicharts v1.3.4. It is written for reviewers and future maintainers who need to understand the calculation choices without reading every code path first.

## References Used

- Anhøj J. Diagnostic value of run chart analysis: using likelihood ratios to compare run chart rules on simulated data series. PLoS ONE, 2015.
- Anhøj J, Olesen AV. Run charts revisited: a simulation study of run chart rules for detection of non-random variation in health care processes. PLoS ONE, 2014.
- NHS England and NHS Making Data Count SPC guidance, especially the practical use of XmR charts, shifts, trends and assurance/variation language.
- Montgomery DC. Introduction to Statistical Quality Control.
- NIST/SEMATECH e-Handbook of Statistical Methods.
- Wheeler DJ. Understanding Variation: The Key to Managing Chaos.

## Run Charts

The default run-chart centre is the median of the active segment. Points equal to the median are ignored for crossing and run-length logic, which follows common Anhøj run-chart practice.

Implemented signals:

- Longest run: the longest sequence of points on one side of the median is compared with expected limits for the number of useful observations.
- Few crossings: the observed number of crossings of the median is compared with expected limits for useful observations.
- `bestbox`: searches deterministic candidate centre values and chooses the centre with the strongest non-signal margin.
- `cutbox`: uses a deterministic cut-point style centre search for compatibility with qicharts-style workflows.

Known deviation: exact probability tables in published run-chart papers are not bundled as external certification data. The implementation is deterministic and tested against internal fixtures and edge cases.

## Individuals and Moving Range Charts

For Individuals charts:

```text
CL = mean(x)
MR_i = abs(x_i - x_{i-1})
MRbar = mean(MR_i)
sigma = MRbar / 1.128
LCL = CL - 3 * sigma
UCL = CL + 3 * sigma
```

For Moving Range charts:

```text
CL = MRbar
LCL = 0
UCL = 3.267 * MRbar
```

When `baseline_points`, `freeze_points`, `breaks` or `recalculation_points` are supplied, the formulas are applied within the active segment. Excluded points remain visible in the output table but are removed from the calculation source and have signal fields cleared.

## NHS XmR Signals

The XmR signal engine records:

- Rule 1: point above UCL or below LCL.
- Shift: sustained points above or below the centre line.
- Trend: consecutive increasing or decreasing points.

`improvement="high is good"` and `improvement="low is good"` convert high/low signals into improvement, concern or neutral labels. The numeric limits do not change; only interpretation changes.

## C Charts

C charts assume a count of nonconformities with a constant area of opportunity.

```text
cbar = mean(c)
sigma = sqrt(cbar)
LCL = max(0, cbar - 3 * sqrt(cbar))
UCL = cbar + 3 * sqrt(cbar)
```

Signals are points below LCL or above UCL.

## P Charts

P charts monitor proportions with variable denominators.

```text
p_i = events_i / n_i
pbar = sum(events) / sum(n)
SE_i = sqrt(pbar * (1 - pbar) / n_i)
LCL_i = max(0, pbar - 3 * SE_i)
UCL_i = min(1, pbar + 3 * SE_i)
```

Denominators must be positive. Segment-specific `pbar` values are used when recalculation periods are present.

## U Charts

U charts monitor rates per unit where denominators can vary.

```text
u_i = events_i / n_i
ubar = sum(events) / sum(n)
SE_i = sqrt(ubar / n_i)
LCL_i = max(0, ubar - 3 * SE_i)
UCL_i = ubar + 3 * SE_i
```

The implementation keeps P-chart proportion logic distinct from U-chart rate logic.

## Xbar and S Charts

Rows are grouped by the x value. For each subgroup:

```text
xbar_i = mean(subgroup_i)
s_i = sample standard deviation(subgroup_i)
n_i = subgroup size
```

For Xbar charts:

```text
grand mean = weighted mean of subgroup means
sbar = mean(s_i)
c4(nbar) = sqrt(2 / (nbar - 1)) * gamma(nbar / 2) / gamma((nbar - 1) / 2)
sigma = sbar / c4(nbar)
LCL_i = grand mean - 3 * sigma / sqrt(n_i)
UCL_i = grand mean + 3 * sigma / sqrt(n_i)
```

For S charts:

```text
CL = sbar
c4_i = c4(n_i)
factor_i = 3 * sqrt(1 - c4_i^2) / c4_i
LCL_i = max(0, sbar * (1 - factor_i))
UCL_i = sbar * (1 + factor_i)
```

Known deviation: constant-table shortcuts such as A3/B3/B4 are not hard-coded. The implementation calculates normal-theory constants from subgroup size to support variable subgroup sizes.

## G Charts

G charts monitor counts between rare events. pyqicharts treats the interval count as non-negative and estimates:

```text
mean interval = mean(g)
p = 1 / (mean interval + 1)
LCL = max(0, log(0.99865) / log(1 - p) - 1)
UCL = max(0, log(0.00135) / log(1 - p) - 1)
```

Signals are unusually short intervals below LCL and unusually long intervals above UCL. Negative intervals raise `ValueError`.

## T Charts

T charts monitor time between events using an exponential-style interval model:

```text
mean interval = mean(t)
LCL = -mean interval * log(0.99865)
UCL = -mean interval * log(0.00135)
```

Signals are unusually short or long intervals. The package does not infer calendar gaps; users should supply already-calculated intervals.

## P-prime and U-prime Charts

Risk-adjusted charts require `observed` and `expected` values. With a denominator:

```text
OE_i = observed_i / expected_i
centre = sum(observed) / sum(denominator)
plot_i = OE_i * centre
```

For P-prime:

```text
expected_probability_i = expected_i / denominator_i
SE_i = centre * sqrt((1 - expected_probability_i) / (expected_probability_i * denominator_i))
```

For U-prime:

```text
SE_i = centre / sqrt(expected_i)
```

Without a denominator, the fallback chart plots observed/expected ratios around a centre of 1:

```text
SE_i = 1 / sqrt(expected_i)
LCL_i = max(0, centre - 3 * SE_i)
UCL_i = centre + 3 * SE_i
```

Zero expected values produce missing ratio/limit fields rather than division-by-zero failures.

## Nelson and Shewhart Rules

Nelson Rules 1-8 are implemented against values standardised by the point-specific centre and sigma. This allows the same rule engine to work with segmented and variable-denominator charts. The Shewhart helper currently exposes the 3-sigma point-beyond-limits rule through the shared signal schema.

## Segmentation and Exclusions

All supported chart families carry:

- `segment_id` and `segment_label`.
- baseline/freeze metadata.
- target, intervention, step-change and phase metadata.
- `excluded` flags.

Excluded observations are retained for auditability but do not contribute to centre lines, limits or signal output. v1.3.4 includes dedicated freeze-point tests and segmented rare-event expected-output fixtures.
