# Telco customer churn prediction (Django)

A small Django web app that predicts whether a telecom customer is likely to cancel their contract (churn). A user fills in a form with the customer's profile (contract type, services, tenure, charges) and the app answers **churn** or **no churn**.

## Data

[IBM Telco Customer Churn](Telcochurn/predict/models/Telco_customer_churn.xlsx) dataset: about 7,000 customers of a fictional telecom provider in California, with their services, account details and whether they left.

Before modelling, the app:
- drops identifiers, location columns and columns that leak the answer (`Churn Label`, `Churn Score`, `CLTV`, `Churn Reason`)
- converts `Total Charges` to numbers and removes the rows where it is empty
- encodes the categorical columns with `OrdinalEncoder`

The model uses 18 features, for example senior citizen, partner, dependents, tenure in months, internet service, online security, tech support, contract type, payment method, monthly charges and total charges.

## Model

- Train/test split: 80/20, stratified on the churn label
- Classifier: support vector machine (`SVC`, RBF kernel, `C=100`, `gamma=0.01`)
- A gradient boosting model is also saved in [`predict/models/gbc.pkl`](Telcochurn/predict/models/gbc.pkl); the web form currently uses the SVM

## Project structure

```
Telcochurn/
├── Telcochurn/          Django settings and URLs
├── predict/
│   ├── views.py         data preparation, model training and prediction
│   └── models/          dataset (xlsx, csv) and saved model (gbc.pkl)
└── template/            HTML pages: home, prediction form, database view
```

## Run it locally

The project was built with Django 3.1 and stores data in MongoDB through `djongo`.

```bash
cd Telcochurn
pip install "django<4" djongo pymongo joblib openpyxl -r requirements.txt
python manage.py runserver
```

Then open http://127.0.0.1:8000, go to the prediction page, fill in the form and submit. The "view database" page needs a MongoDB server running on `localhost:27017`.

## Limitations and next steps

- The SVM is retrained on every prediction request; it should be trained once and loaded from disk.
- Some form branches in `views.py` are mis-indented, so certain combinations of answers can raise an error.
- No evaluation metrics are reported yet (accuracy, recall on churners, ROC AUC).
- `SECRET_KEY` and `DEBUG = True` are hard-coded in `settings.py`, which is fine for local use only.

Next steps: move training into a separate script, report metrics, explain the main churn drivers, and deploy a demo.

## Author

Ami Samyra Ouedraogo · [GitHub](https://github.com/amisamyra99) · [LinkedIn](https://www.linkedin.com/in/ouedraogo-ami-samyra/)
