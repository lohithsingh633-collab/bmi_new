# BMI Calculator Streamlit App

A beginner-friendly Streamlit application that:

- Takes name, age, gender, height and weight
- Calculates BMI
- Displays an adult BMI category
- Provides general meal suggestions
- Provides light exercise suggestions
- Saves records to `bmi_records.csv`
- Allows saved records to be downloaded as CSV

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, usually:

`http://localhost:8501`

## Important note about deployment

The CSV approach is useful for learning and for local use. On a cloud deployment, local files should not be treated as a permanent database. For a production-style app, replace CSV storage with a persistent database or cloud spreadsheet/database.

## Health note

This app is designed for adults aged 18+. BMI is a screening measure, not a diagnosis. The meal and exercise suggestions are general educational suggestions and are not personalized medical advice.
