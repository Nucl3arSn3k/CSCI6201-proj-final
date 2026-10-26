## Project title
The smell of Shaw

## Team member names
Kestor Brown

## Selected datasets
Going to look at the 311 city service requests from 2025 for Lab 2, then use the Alcohol License dataset later.

## Problem family
Regression

## Proposed research questions
Are sanitation-type complaints in Shaw spatially associated with bar locations?
Can bar density and other local features predict how many complaints the area receives?

## Progress
Loaded and explored the full dataset, defined "smell-type" requests, aggregated requests into 1,758 grid cells, made two figures, and ran a baseline plus a linear regression.

A baseline that always predicts the training mean has MAE 40.3. A linear regression using one feature, the number of other (non-smell-type) 311 requests in the grid cell, reduces MAE to 27.9 (R² = 0.41) on a 20% held-out test set. This feature is a stand-in for the bars until the alcohol data is added.

## Figures
I drew a bar chart of solid-waste requests. They are predominantly scheduled-service categories such as Bulk Collection and Yard Waste. Complaint-style categories follow, and the rest of the top 10 is much smaller. This is why I narrowed the analysis to a smaller list of nuisance-related request types, because the full group includes some basic logistics.

For the scatter plot, I mapped the smell-type complaints and drew a basic bounding box around the Shaw neighborhood to see if complaints concentrate there. Requests appear across most of the city but cluster in the dense central neighborhoods. The Shaw box sits inside one of those clusters, holding 3.7% of all smell-type requests (2,694 of 71,997).

## Install and run instructions
Clone the repo, make sure you have the required libraries (pandas, matplotlib and scikit-learn),as well as a Python version 3.10 or newer. Then run the following from project root:

    python src/analysis.py

## Next steps for final project
- **What is working:** the full pipeline (load, explore, plot, grid-cell table, baseline and linear regression).
- **What needs work:** the model has no bar feature yet, so it can't answer the research questions. The target is also heavily skewed (median 18, mean 41, max 533).
- **What I plan to add:** join the alcohol license locations to add bar count per cell, rerun the regression, and compare against this baseline.
- **Feedback I'd like:** Is my grid "cell" size reasonable for analysis?
