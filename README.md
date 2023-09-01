
NextPill is an AI tool that tackles the painful prior authorization process, empowering physicians to prescribe a medication that insurance companies will most likely approve and cover given a patient's medical conditions. The pain point is that physicians have to play a "guessing game" to prescribe medication that they anticipate insurance will pay for. This tool provides insights about the relationship between patient health conditions, medication prescribed, and insurance amount paid to reduce this pain point. 

Our tool trained a random forest AI model based on claims data from the Tuva project (https://thetuvaproject.com/). The specific attributes we looked at within the data were IDC diagnostic codes (representing the patient's symptoms or health conditions), NDC codes (the prescribed medication), and amount paid by insurance (whether they covered it or paid $0). Random forest uses these attributes to make decision trees to predict given a set of diagnostic codes, what medication prescription will likely be covered by insurance.

Our tool has been deployed as an app on Health Universe: https://apps.healthuniverse.com/ceo-wfu-oev. It features a UI that physicians can select the number of patient diagnostic codes they want to enter and then the codes themselves. Once they submit, our tool will output a NDC code recommendation. This code represents the medication prescription that has the highest chance of being covered by insurance. We currently do not have a mapping of IDC and NDC codes to the corresponding English version of the codes. When selecting your IDC code from the dropdown, use this website to look up the matching symptom (https://www.icd10data.com/). Once you submit and get your NDC code recommendation, use this website to find the corresponding prescription (https://ndclist.com/?s=&Finished=&Unfinished=&Excluded=&Compounded=).

Learn more about NextPill in this pitch deck: https://docs.google.com/presentation/d/1lH2XJtg0xNEZSWBVU9D_vQ2oHstIFqGwNcGjV795bd0/edit?usp=sharing

To run the tool, git clone this repository. Run "pip install -r requirements.txt" so you have all requirements locally. Run "uvicorn main:app --reload" to see the application deployed locally.

Built Using:
* Flask
* Bootstrap
* Random Forest
