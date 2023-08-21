This project was done for the XPrimaryCare Healthcare+AI hackathon: https://hackathon.xprimarycare.com/
We are team NextPill and we won the award for best project on the "Care Insights" track.

NextPill is an AI tool that empowers physicians to prescribe a medication that insurance companies will most likely approve and cover given a patient's medical conditions. The pain point is that physicians have to play a "guessing game" to prescribe medication that they anticipate insurance will pay for. This tool provides insights about the relationship between patient health conditions, medication prescribed, and insurance amount paid to reduce this pain point.

Our tool trained a random forest AI model on Tuva claims data. The specific attributes we looked at within the data were diagnostic codes (representing the patient's health conditions), NDC codes (the prescribed medication), and amount paid by insurance (whether they covered it or paid $0). Random forest uses these attributes to make decision trees to predict given a set of diagnostic codes, what medication prescription will likely be covered by insurance.

Our tool features a UI that physicians can select the number of patient diagnostic codes they want to enter and then the codes themselves. Once they submit, our tool will output a NDC code recommendation.

To run the tool, git clone this repository. Run "pip install -r requirements.txt" so you have all requirements locally. Run "python app.py" to see the application deployed locally.

Built Using:
* Flask
* Bootstrap
* Random Forest
