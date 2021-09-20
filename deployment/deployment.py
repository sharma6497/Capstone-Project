# -*- coding: utf-8 -*-

import flask
import pandas as pd
import pickle


app=flask.Flask(__name__,template_folder='templates')

@app.route('/',methods=['GET','POST'])
def main():
    if flask.request.method == 'GET' :
        return(flask.render_template('final_form.html'))
    
    if flask.request.method=='POST':
        purchaser_type=flask.request.form['Purchaser_Type']
        loan_type=flask.request.form['Loan_Type']
        loan_purpose=flask.request.form['Loan_Purpose']
        open_end_line_of_credit=flask.request.form['Open-End_Line_of_Credit']
        loan_to_value_ratio=flask.request.form['Loan_to_value_ratio']
        lien_status=flask.request.form['Lien_status']
        income=flask.request.form['Income']
        debt_to_income_ratio=flask.request.form['Debt_to_Income_Ratio']
        occupancy_type=flask.request.form['Occupancy_Type']
        interest_only_payment=flask.request.form['Interest_only_payment']
        applicant_age=flask.request.form['Applicant_Age']
        co_applicant_age=flask.request.form['Co-Applicant_Age']
        submission=flask.request.form['submission']
        initially_payable=flask.request.form['initially_payable']
        high_cost_mortgage=flask.request.form['High_Cost_Mortgage']
        
        test=pd.DataFrame([[purchaser_type,loan_type,loan_purpose,open_end_line_of_credit,
                            loan_to_value_ratio,lien_status,income,debt_to_income_ratio,
                            occupancy_type,interest_only_payment,applicant_age,co_applicant_age,submission,
                            initially_payable,high_cost_mortgage]],
                          columns=['purchaser_type','loan_type','loan_purpose','open-end_line_of_credit',
                                   'loan_to_value_ratio','lien_status','income','debt_to_income_ratio','occupancy_type',
                                   'interest_only_payment','applicant_age','co-applicant_age','submission_of_application',
                                   'initially_payable_to_institution','high_cost_mortgage'])
        cols=list(test.columns)
        cols.remove('income')
        for col in cols:
            pick=pickle.load(open(col,'rb'))
            test[col]=test[col].map(pick)
            rf_model=pickle.load(open('full_pipeline','rb'))
        prediction=rf_model.predict(test)
        if prediction == 1:
            op='Approved'
        elif prediction == 0:
            op='Rejected'
        
        return flask.render_template('final_form.html', prediction_text='Loan Status: {}'.format(op))
        
if __name__=='__main__':
    app.run()