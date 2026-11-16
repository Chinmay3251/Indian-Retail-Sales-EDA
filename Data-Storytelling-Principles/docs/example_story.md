# Example Data Story — Retail Sales Performance

> This story uses synthetic practice data, not actual company results.

## Audience and decision
**Audience:** Sales manager  
**Decision:** Decide where to focus a sales-improvement review.

## Central message
Revenue is distributed unevenly across product categories and regions. The team should review the largest revenue contributors alongside profit and discount patterns rather than treating sales alone as success.

## Context
The dataset contains transaction-level sales, profit, quantity, discount, category, region, and order date fields. Run the analysis script to generate exact summary values and charts.

## Evidence to review
- **Category:** Identify the highest-sales category and compare its profit contribution.
- **Region:** Compare sales, profit, and profit margin by region.
- **Time:** Review monthly sales for sustained movement, seasonality, and unusual spikes.
- **Discount:** Explore the relationship between discount and profit. This is descriptive, not proof of causation.

## Business implication
Use the analysis to decide where to investigate first. A high-revenue segment may not have the strongest profit contribution.

## Recommended next steps
1. Review category-region combinations with high sales but weak profit.
2. Inspect discount levels and product mix in those combinations.
3. Test one targeted change in a limited segment or period.
4. Compare sales, profit, and margin against a comparable baseline.

## Success measures
Track revenue, total profit, profit margin, average discount, and order count before and after the test. Define the comparison period and success threshold in advance.

## Limitations
The dataset is synthetic. The analysis is observational and does not establish causality. Results depend on data quality, time window, and metric definitions.
