# Bank Marketing Prediction

README work in progress

Simple project to help me understand how to read data with a model. Data is from https://archive.ics.uci.edu/dataset/222/bank+marketing

Removed columns:
- Duration: Info is found after the call is over, would be data leakage
- Campaign: It counts the current call, info isn't fully known before the call
- pdays: Most pdays are 999, meaning N/A. poutcome and previous already have most of the same info

Keep unknown as its own category to stay consistent and prevent guessing.
Removed 12 duplicate rows
Converted y/n to 1/0

Baseline: 88.7% accuracy by always prediciting no

precision    recall  f1-score   support

           0       0.95      0.89      0.92      7308
           1       0.41      0.64      0.50       928

    accuracy                           0.86      8236
   macro avg       0.68      0.76      0.71      8236
weighted avg       0.89      0.86      0.87      8236
0.8117661266349584
Random Tree with depth=10 table

precision    recall  f1-score   support

           0       0.95      0.85      0.90      7308
           1       0.36      0.65      0.46       928

    accuracy                           0.83      8236
   macro avg       0.65      0.75      0.68      8236
weighted avg       0.88      0.83      0.85      8236
0.8007070074363476
Logistic Regression

precision    recall  f1-score   support

           0       0.93      0.91      0.92      7308
           1       0.40      0.47      0.43       928

    accuracy                           0.86      8236
   macro avg       0.67      0.69      0.68      8236
weighted avg       0.87      0.86      0.87      8236
0.7694521414887795
Random Tree, no max depth
print(model.score(X_train, y_train), model.score(X_test, y_test))

Top 10 Most Important Features:
          Feature  Importance
      nr.employed    0.196914
        euribor3m    0.189032
     emp.var.rate    0.108650
    cons.conf.idx    0.077243
   cons.price.idx    0.074457
 poutcome_success    0.063603
              age    0.037799
         previous    0.030368
contact_telephone    0.029243
        month_may    0.025504

Overfitting: 0.9795081967213115 0.8623118018455561

Yes Rate By:
Job:
            job      n  yes_rate_pct
0         student    875          31.4
1         retired   1718          25.3
2      unemployed   1014          14.2
3          admin.  10419          13.0
4         unknown    330          11.2
5      management   2924          11.2
6      technician   6739          10.8
7   self-employed   1421          10.5
8       housemaid   1060          10.0
9    entrepreneur   1456           8.5
10       services   3967           8.1
11    blue-collar   9253           6.9
Students are the highest, which indirectly shows younger people say yes more

Month:
 month      n  yes_rate_pct
0   mar    546          50.5
1   dec    182          48.9
2   sep    570          44.9
3   oct    717          43.9
4   apr   2631          20.5
5   aug   6176          10.6
6   jun   5318          10.5
7   nov   4100          10.1
8   jul   7169           9.0
9   may  13767           6.4
Busier months have lower rates.

poutcome:
poutcome      n  yes_rate_pct
0      success   1373          65.1
1      failure   4252          14.2
2  nonexistent  35551           8.8
Repeat customers are more likly to say yes

By age group
age_group      n  yes_rate_pct
0       65+    662          47.3
1  under 25   1067          24.0
2     25-34  13684          12.2
3     50-64   7391          11.6
4     35-49  18372           8.4