# Bank Marketing Prediction

Simple project to help me understand how to read data with a model. Data is from https://archive.ics.uci.edu/dataset/222/bank+marketing

Removed columns:
- Duration: Info is found after the call is over, would be data leakage
- Campaign: It counts the current call, info isn't fully known before the call
- pdays: Most pdays are 999, meaning N/A. poutcome and previous already have most of the same info

Keep unknown as its own category to stay consistent and prevent guessing.
Removed 12 duplicate rows
Converted y/n to 1/0