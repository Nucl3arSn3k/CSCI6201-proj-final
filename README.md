*Project Title*: The smell of Shaw

*Team Member Names*: Kestor Brown

*Selected Dataset(s)*: Going to look at teh Alochol_License Buisness set for lab 2 but am alsoi going to use the 311 city service requests from 2025 later.

*Problem family*: Regression

*Proposed research questions*:Are sanitation-type complaints in Shaw spatially associated with bar locations? 
Can bar density and other local features predict how many complaints the area receives? 

*State of progress*: Working towards getting this towards the lab2 state of completion.

*Next Steps for Final Project:* Include the new dataset with bars and start mapping the 311 reqeusts around them.

Currently, I ran the linear regression on the number of non-sanitation 311 requests in the grid cell as a stand-in for the bars.
A baseline that always predicts the training has MAE 40.3. Running a linear regression using one feature, the number of non-sanitation 311 requests in the grid cell, reduces MAE to 27.9 (R² = 0.41) on a 20% held-out test set.

I'm going to add the dataset for bar count per cell once I start utilizing the alchol data then run the prediction again.

Drew a barchart for solid waste requests.
Predominantly scheduled-service categories such as Bulk Collection and Yard Waste. Complaint-style categories follow, and the rest of the top 10 is much smaller. This is why I narrowed the analysis to a smaller list of nuisance-related request types, because the full group includes some basic logistics.

As for the scatterplot, I just used it to get a general sense for where the requests holistically cluster.
