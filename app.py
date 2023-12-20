# Import Streamlit library
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from io import BytesIO

def ask_for_csv():
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    if not uploaded_files:
        return None

    valid_dataframes = []
    for uploaded_file in uploaded_files:
        # Check file extension
        if uploaded_file.name[-3:] != "csv":
            st.error(f"Only CSV files are accepted. The file {uploaded_file.name} is not a CSV.")
            continue

        # Try reading the CSV file into a DataFrame
        try:
            dataframe = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading {uploaded_file.name}: {e}")
            continue
        
        # Check if the columns match the expected format
        expected_columns = [
            "Fundamental Rights", "Education and Tutorials", "Human Autonomy", 
            "Human Oversight", "Governance Mechanisms", "Resilience to Attack and Security", 
            "General Safety", "Accuracy", "Reliability and Reproducibility", 
            "Respect for Privacy and Data Protection", "Access to Data", 
            "Transparency", "Diversity, Non-discrimination and Fairness", 
            "Societal and Environmental Wellbeing", "Accountability", "Timestamp"
        ]
        if dataframe.columns.tolist() != expected_columns:
            st.error(f"The file {uploaded_file.name} does not have the expected columns.")
            continue
        try:
            # Convert 'Timestamp' column to datetime objects using the correct format
            dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'], format='mixed')
            
            # Then, since you want to display only the date part without the time,
            # you can format it to a string without the time component
            dataframe['Timestamp'] = dataframe['Timestamp'].dt.strftime('%m/%d/%Y')
        except Exception as e:
            st.error(f"Error converting the Timestamp column in {uploaded_file.name}: {e}")
            continue

        # If the DataFrame is valid, add it to the list
        valid_dataframes.append(dataframe)

    # If there are valid DataFrames, concatenate them
    if valid_dataframes:
        combined_dataframe = pd.concat(valid_dataframes, ignore_index=True)
        return combined_dataframe
    else:
        return None

# Plot the spider Plot 
def plot_spider_chart(df):
    # Exclude the 'Timestamp' column when finding the max value for the radial axis range
    max_value = df[df.columns.difference(['Timestamp'])].max().max()
    
    fig = go.Figure()
    
    for index, row in df.iterrows():
        # Convert 'Timestamp' to datetime if it's a string, otherwise use it directly
        timestamp = pd.to_datetime(row['Timestamp']) if isinstance(row['Timestamp'], str) else row['Timestamp']
        # Format the 'Timestamp' as a string for the trace name
        trace_name = timestamp.strftime("%Y-%m-%d") if not isinstance(row['Timestamp'], str) else row['Timestamp']
        
        fig.add_trace(go.Scatterpolar(
            r=row[:-1],  # all the data except 'Timestamp'
            theta=df.columns[:-1],  # assuming 'Timestamp' is the last column
            fill='toself',
            name=trace_name
        ))
    
    # Set the layout for the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value]  # use the calculated max_value
            )
        ),
        showlegend=True
    )
    
    return fig

# Main app
def main():
    if 'update_report_initiated' not in st.session_state:
        st.session_state['update_report_initiated'] = False
    if 'generate_report_initiated' not in st.session_state:
        st.session_state['generate_report_initiated'] = False
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False
    if 'combined_data' not in st.session_state:
        st.session_state['combined_data'] = pd.DataFrame()
    if 'csv' not in st.session_state:  # Initialize 'csv' in session state
        st.session_state['csv'] = ""


    st.title("AI Guidelines Questionnaire for Companies")

    generate_report_button = st.button('Generate report from previous data')
    update_report_button = st.button('Update report with new questionnaire entry')

    if update_report_button:
        st.session_state['update_report_initiated'] = True
        st.session_state['generate_report_initiated'] = False
    if generate_report_button:
        st.session_state['generate_report_initiated'] = True
        st.session_state['update_report_initiated'] = False

    if st.session_state['update_report_initiated']:
        st.write("""If you would like to track the progress relative to a previous report, please submit a previously 
                 generated csv. If not, please leave it blank.""")
        previous_data = ask_for_csv()
                    
        # Create a list to store answers
        answers = []
        answers_dict = {"Fundamental Rights" : [0, 0], "Education and Tutorials" : [0, 0], "Human Autonomy" : [0, 0], 
                        "Human Oversight" : [0, 0], "Governance Mechanisms" : [0, 0], "Resilience to Attack and Security" : [0, 0], 
                        "General Safety" : [0, 0], "Accuracy" : [0, 0], "Reliability and Reproducibility" : [0, 0], 
                        "Respect for Privacy and Data Protection" : [0, 0], "Access to Data" : [0, 0], 
                        "Transparency" : [0, 0], "Diversity, Non-discrimination and Fairness" : [0, 0], 
                        "Societal and Environmental Wellbeing"  : [0, 0], "Accountability" : [0, 0]}
        
        def update_dict(selected_index, category):
            answers_dict[category][1] += 2
            if selected_index == 0:
                answers_dict[category][0] += 2
            elif selected_index == 1:
                answers_dict[category][0] += 1
            

        # Question 1
        st.markdown("## SECTION 1: HUMAN AGENCY AND OVERSIGHT")
        st.markdown("### FUNDAMENTAL RIGHTS")
        st.markdown("""##### How are you dealing with the effect of the application on the rights to safety, health, non-discrimination, and freedom of association?
    """)
        q1_options = [
            "We’ve performed a clear analysis in response to these principles and can provide details.",
            "We have partially/informally considered these principles but no specific details can be provided.",
            "We have not considered these issues yet.",
            "We consider that these issues are not applicable to our case."]
        q1 = st.radio("", q1_options)

        selected_index = q1_options.index(q1)

        update_dict(selected_index, 'Fundamental Rights')

        # Question 2
        st.markdown("### EDUCATION AND TUTORIALS")
        category = "Education and Tutorials"
        st.markdown("##### Are the end users or subjects informed that they are interacting with an AI system and that a decision,content, advice or outcome is a result of an algorithmic decision?")
        q2_options = ["""Users are aware of both.""", 
                    """Users are aware that they are interacting with an AI system, but aren’t aware of how the system comes to a final answer. """, 
                    """We have not considered these issues yet.""",
                    """We consider that these issues are not applicable to our case."""]  
        q2 = st.radio("", q2_options)

        selected_index = q2_options.index(q2)

        update_dict(selected_index, category)

        # Question 3
        st.markdown("### HUMAN AUTONOMY")
        category = "Human Autonomy"
        st.markdown("##### Could the AI system affect human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way?")

        q3_options = [
            "Yes, the system affects human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way.",
            "The system might affect human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way.",
            "We have not considered these issues yet. ",
            "We consider that these issues are not applicable to our case. "]
        q3 = st.radio("", q3_options)

        selected_index = q3_options.index(q3)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        update_dict(selected_index, category)

        # Question 4
        if answers.pop() == 1 or answers.pop() == 0:
            st.markdown("##### Was any procedure put in place to avoid that the AI system inadvertently affects human autonomy?")
            q4_options = [
                "Yes, it a procedure was put in place to avoid that the AI system inadvertently affects human autonomy",
                "No procedure was put in place",
                "We have not considered these issues yet.",
                "We consider that these issues are not applicable to our case. "
            ]
            q4 = st.radio("", q4_options)

            selected_index = q4_options.index(q4)

            update_dict(selected_index, category)

        # Question 5
        st.markdown("##### Does the AI risk creating human attachment, stimulating addictive behavior, generating over-reliance by end users or manipulating user behavior?")
        q5_options = [
            "We have performed a clear analysis and implemented measures to deal with possible negative consequences for the end users or subjects in case they develop a disproportionate attachment to the AI system.",
            "We have partially/informally considered these principles but no specific details can be provided.",
            "We have not considered these issues yet.",
            "We consider that these issues are not applicable to our case."
        ]
        q5 = st.radio("", q5_options)

        selected_index = q5_options.index(q5)

        update_dict(selected_index, category)

        # Question 6
        st.markdown("### HUMAN OVERSIGHT")
        category = "Human Oversight"
        st.markdown("##### How easy is it to deactivate/abort an operation while needed or remove the system and data once users are no longer interested or need the system?")
        q6_options = [
            "Very easy, either through clear instructions or automatically by a sunset clause.",
            "Instructions on how to deactivate or remove the system and data are unclear. ",
            "We have not considered these issues yet",
            "We consider that these issues are not applicable to our case."]
        q6 = st.radio("", q6_options)

        selected_index = q6_options.index(q6)
        update_dict(selected_index, category)

        st.markdown("### GOVERNANCE MECHANISMS")
        category = "Governance Mechanisms"
        st.markdown("##### *Glossary* \n *Self Learning Systems : Refers to a system's autonomous ability to acquire knowledge, adapt, and improve over time without direct human intervention*")
        st.markdown("*Human-in-the-loop: Refers to the capability for human intervention in every decision cycle of the system.*")
        st.markdown("*Human-on-the-loop: Refers to the capability for human intervention during the decision cycle of the system.*")
        st.markdown("*Human-in-command: Refers to the capability to oversee the overall activity of the AI system (including its broader economic, societal, legal and ethical impact)*")
        # Question 7
        st.markdown("##### Self-learning systems require specialized oversight measures, including regular assessments of their evolving algorithms, continuous validation against predefined ethical guidelines, and proactive monitoring for potential biases or unintended consequences, coupled with a robust framework for adaptability and intervention in response to emergent issues. Does your system implement these measures?")
        q7_options = [
            "Yes, the measures are implemented wholly.",
            "The measures are implemented partially/informally. ",
            "We have not considered these issues yet.",
            "We consider that these issues are not applicable to our case."]
        q7 = st.radio("", q7_options)

        selected_index = q7_options.index(q7)
        update_dict(selected_index, category)

        # Question 8: Human-in-the-loop (HITL) Systems
        st.markdown("##### Human-in-the-loop (HITL) systems, where human input is integrated into automated processes, require unique oversight measures, including regular audits of human-machine interactions, continuous training for human operators to adapt to evolving system behavior, and transparent communication channels to address potential ethical concerns and biases introduced during collaboration.Does your system implement these measures?")
        q8_options = [
            "Yes, the measures are implemented wholly. (2)",
            "The measures are implemented partially/informally. (1)",
            "We have not considered these issues yet. (0)",
            "We consider that these issues are not applicable to our case. (N/A)"
        ]
        q8 = st.radio("", q8_options)
        selected_index = q8_options.index(q8)
        update_dict(selected_index, category)

        # Question 9: Hybrid-operationalized Task Learning (HOTL) Systems
        st.markdown("##### Hybrid-operationalized task learning (HOTL) systems demand specialized oversight measures, encompassing periodic evaluations of both automated and human-performed tasks, iterative refinement of shared decision-making protocols, and a robust feedback loop to ensure seamless coordination and alignment between machine and human intelligence.Does your system implement these measures?")
        q9_options = [
            "Yes, the measures are implemented wholly. (2)",
            "The measures are implemented partially/informally. (1)",
            "We have not considered these issues yet. (0)",
            "We consider that these issues are not applicable to our case. (N/A) "
        ]
        q9 = st.radio("", q9_options)
        selected_index = q9_options.index(q9)
        update_dict(selected_index, category)

        # Question 10: Human-in-the-Critical Path (HIC) Systems
        st.markdown("##### Human-in-the-critical path (HIC) systems necessitate distinctive oversight measures, involving continuous monitoring of human involvement in mission-critical processes, real-time performance assessments to identify potential bottlenecks or errors, and a comprehensive training framework to enhance human operators' proficiency in handling high-stakes situations within the system.Does your system implement these measures?")
        q10_options = [
            "Yes, the measures are implemented wholly. (2)",
            "The measures are implemented partially/informally. (1)",
            "We have not considered these issues yet. (0) ",
            "We consider that these issues are not applicable to our case. (N/A)"
        ]
        q10 = st.radio("", q10_options)
        selected_index = q10_options.index(q10)
        update_dict(selected_index, category)

        # Section 2
        st.markdown("## SECTION 2: TECHNICAL ROBUSTNESS AND SAFETY")
        st.markdown("### RESILIENCE TO ATTACK AND SECURITY")
        category = "Resilience to Attack and Security"
        # Question 11: Adversarial, Critical, or Damaging Effects of AI System
        st.markdown("##### Could the AI system have adversarial, critical or damaging effects (e.g. to human or societal safety) in case of intended or unintended problems such as design or technical faults, defects, outages, attacks, misuse, inappropriate or malicious code?")
        q11_options = [
            "The AI system **does not have** adversarial, critical or damaging effects (e.g. to human or societal safety) in case of intended or unintended problems (2)",
            "The AI system **might have** adversarial, critical or damaging effects (e.g. to human or societal safety) in case of intended or unintended problems (1)",
            "The AI system **has** adversarial, critical or damaging effects (e.g. to human or societal safety) in case of intended or unintended problems (0)",
            "We have not considered these issues yet as it isn’t relevant (N/A)"
        ]
        q11 = st.radio("", q11_options)
        selected_index = q11_options.index(q11)
        update_dict(selected_index, category)

        # Question 12: Cybersecurity Certification of AI System
        st.markdown("##### Is the AI system certified for cybersecurity (e.g the certification scheme created by the Cybersecurity Act in Europe) or is it compliant with specific security standards?")
        q12_options = [
            "The AI system **is** certified for cybersecurity. (2)",
            "The AI system **is not** certified for cybersecurity. (1)",
            "We consider that these issues are not applicable to our case. (N/A)"
        ]
        q12 = st.radio("", q12_options)
        selected_index = q12_options.index(q12)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1:
            # Question 13: Consideration of Vulnerabilities and Potential Entry Points for Attacks
            st.markdown("##### Did you consider the different types of vulnerabilities and potential entry points for attacks such as: Data poisoning (i.e. manipulation of training data); Model evasion (i.e. classifying the data according to the attacker’s will); Model inversion (i.e. infer the model parameters)?")
            q13_options = [
                "Different types of vulnerabilities and potential entry points for attacks were formally and thoroughly considered.(2)",
                "Different types of vulnerabilities and potential entry points for attacks were informally/partially considered.(1)",
                "We have not considered these issues yet. (0)",
                "We consider that these issues are not applicable to our case. (N/A)"
            ]
            q13 = st.radio("", q13_options)
            selected_index = q13_options.index(q13)
            update_dict(selected_index, category)


        # Question 13
        st.markdown("### GENERAL SAFETY")
        category = "General Safety"
        st.markdown("##### Did you define risks, risk metrics and risk levels of the AI system in each specific use case?")
        q14_options = [
            "We have defined comprehensive risks, established risk metrics, and determined risk levels specific to each use case of our AI system. We can provide detailed insights into our risk assessment methodologies.",
            "We have partially or informally defined risks, considered risk metrics, and assessed risk levels for our AI system in specific use cases, but specific details on our approach may not be available at this time.",
            "We have not specifically defined risks, established risk metrics, or determined risk levels for our AI system in each specific use case.",
            "We consider that defining risks, risk metrics, and risk levels is not applicable to our specific AI system or use case."]
        q14 = st.radio("", q14_options)

        selected_index = q14_options.index(q14)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        # Question 15
        if answers.pop() == 1 or answers.pop() == 0:
            st.markdown("##### Did you put in place a process to continuously measure and assess risks? ")
            q15_options = [
                "We have implemented a robust process to continuously measure and assess risks associated with our AI system. We can provide detailed information on our ongoing risk measurement and assessment procedures.",
                "We have partially or informally put in place a process to continuously measure and assess risks for our AI system, but specific details on our approach may not be available at this time.",
                "We have not established a specific process to continuously measure and assess risks associated with our AI system.",
                "We consider that implementing a process for continuous measurement and assessment of risks is not applicable to our specific AI system or use case."]
            q15 = st.radio("", q15_options)

            selected_index = q15_options.index(q15)
            update_dict(selected_index, category)

            # Question 16
            st.markdown("##### Did you inform end-users and subjects of existing or potential risks?")
            q16_options = [
                "We have proactively informed end-users and subjects of both existing and potential risks associated with our AI system. We can provide detailed insights into our communication strategies regarding risks.",
                "We have partially or informally informed end-users and subjects of existing or potential risks, but specific details on our communication approach may not be available at this time.",
                "We have not specifically informed end-users and subjects of existing or potential risks associated with our AI system.",
                "We consider that informing end-users and subjects of existing or potential risks is not applicable to our specific AI system or use case."]
            q16 = st.radio("", q16_options)

            selected_index = q16_options.index(q16)
            update_dict(selected_index, category)
        
        # Question 17
        st.markdown("##### Did you identify the possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences?")
        q17_options = [
            "Possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences were identified and fall back plans were put into place.",
            "Possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences were partially identified and fall back plans might have been put into place.",
            "We have not considered these issues yet.",
            "We consider that these issues are not applicable to our case."]
        q17 = st.radio("", q17_options)

        selected_index = q17_options.index(q17)
        update_dict(selected_index, category)

        # Question 18
        st.markdown("##### Did you assess the risk of possible malicious use, misuse or inappropriate use of the AI system?")
        q18_options = [
            "The risk of possible malicious use, misuse or inappropriate use of the AI system was assessed.",
            "The risk of possible malicious use, misuse or inappropriate use of the AI system was not assessed.",]
        q18 = st.radio("", q18_options)

        selected_index = q18_options.index(q18)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        answers_dict[category][1] += 2
        if selected_index == 0:
            answers_dict[category][0] += 2

        if answers.pop() == 0:
            # Question 19
            st.markdown("##### Did you define safety criticality levels (e.g. related to human integrity) of the possible consequences of faults or misuse of the AI system?")
            q19_options = [
                "Safety criticality levels (e.g. related to human integrity) of the possible consequences of faults or misuse of the AI system were clearly defined.",
                "Safety criticality levels (e.g. related to human integrity) of the possible consequences of faults or misuse of the AI system were not defined.",
            ]
            q19 = st.radio("", q19_options)
            answers_dict[category][1] += 1
            selected_index = q19_options.index(q19)
            if selected_index == 0:
                answers_dict[category][0] += 1
        
        
        st.markdown("### ACCURACY")
        category = "Accuracy"
        # Question 20
        st.markdown("##### Did you assess what level and definition of accuracy would be required in the context of the AI system and use case?")
        q20_options = [
            "We have conducted a comprehensive assessment to determine the required level and definition of accuracy for our AI system in the context of the specified use case and can provide detailed information.",
            "We have partially or informally considered the required level and definition of accuracy for our AI system in the context of the specified use case, but specific details cannot be provided at this time.",
            "We have not undertaken an assessment to determine the required level and definition of accuracy for our AI system in the context of the specified use case.",
            "We consider that assessing the required level and definition of accuracy is not applicable to our specific AI system or use case."]
        q20 = st.radio("", q20_options)

        selected_index = q20_options.index(q20)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 21
            st.markdown("##### Did you assess how accuracy is measured and assured?")
            q21_options = [
                "We have conducted a thorough assessment to understand how accuracy is measured and assured for our AI system, and we can provide detailed information on our methodology.",
                "We have partially or informally considered the measurement and assurance of accuracy for our AI system, but specific details on our approach may not be available at this time.",
                "We have not undertaken an assessment regarding how accuracy is measured and assured for our AI system.",
                "We consider that assessing how accuracy is measured and assured is not applicable to our specific AI system or use case."]
            q21 = st.radio("", q21_options)

            selected_index = q21_options.index(q21)
            update_dict(selected_index, category)
        
        
        # Question 22
        st.markdown("##### Did you put in place measures to ensure that the data used is comprehensive and up to date?")
        q22_options = [
            "We have implemented robust measures to ensure that the data used in our AI system is comprehensive and up to date, and we can provide detailed insights into our data management practices.",
            "We have partially or informally considered measures to ensure the comprehensiveness and currency of the data used in our AI system, but specific details on our approach may not be available at this time.",
            "We have not put in place specific measures to ensure the comprehensiveness and up-to-dateness of the data used in our AI system.",
            "We consider that putting in place measures for data comprehensiveness and currency is not applicable to our specific AI system or use case."]
        q22 = st.radio("", q22_options)

        selected_index = q22_options.index(q22)
        update_dict(selected_index, category)
        
        # Question 23
        st.markdown("##### Did you put in place measures in place to assess whether there is a need for additional data, for example to improve accuracy or to eliminate bias?")
        q23_options = [
            "We have implemented measures to assess whether there is a need for additional data, such as to enhance accuracy or mitigate bias, and we can provide detailed insights into our data evaluation practices.",
            "We have partially or informally considered measures to assess the need for additional data, but specific details on our approach may not be available at this time.",
            "We have not put in place specific measures to assess whether there is a need for additional data to improve accuracy or eliminate bias.",
            "We consider that assessing the need for additional data is not applicable to our specific AI system or use case."]
        q23 = st.radio("", q23_options)

        selected_index = q23_options.index(q23)
        update_dict(selected_index, category)
        
        st.markdown("### RELIABILITY AND REPRODUCIBILITY")
        category = "Reliability and Reproducibility"
        # Question 24
        st.markdown("##### Did you put in place a strategy to monitor and test if the AI system is meeting the goals, purposes and intended applications?")
        q24_options = [
            "We have implemented a comprehensive strategy to monitor and test whether the AI system is meeting its goals, purposes, and intended applications. We can provide detailed insights into our monitoring and testing methodologies.",
            "We have partially or informally considered a strategy to monitor and test the alignment of the AI system with its goals, purposes, and intended applications, but specific details on our approach may not be available at this time.",
            "We have not put in place a specific strategy to monitor and test whether the AI system is meeting its goals, purposes, and intended applications.",
            "We consider that implementing a strategy to monitor and test alignment is not applicable to our specific AI system or use case."]
        q24 = st.radio("", q24_options)

        selected_index = q24_options.index(q24)
        update_dict(selected_index, category)

        # Question 25
        st.markdown("##### Did you test whether specific contexts or particular conditions need to be taken into account to ensure reproducibility?")
        q25_options = [
            "We have conducted thorough testing to determine whether specific contexts or particular conditions need to be taken into account to ensure the reproducibility of our AI system. We can provide detailed information on our testing procedures.",
            "We have partially or informally considered testing for specific contexts or conditions related to reproducibility, but specific details on our approach may not be available at this time.",
            "We have not conducted specific tests to assess whether particular contexts or conditions need to be considered for ensuring the reproducibility of our AI system.",
            "We consider that testing for specific contexts or conditions related to reproducibility is not applicable to our specific AI system or use case."]
        q25 = st.radio("", q25_options)

        selected_index = q25_options.index(q25)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 26
            st.markdown("##### Did you put in place verification methods to measure and ensure different aspects of the system's reliability and reproducibility?")
            q26_options = [
                "We have implemented verification methods to measure and ensure various aspects of the system's reliability and reproducibility. We can provide detailed insights into our verification processes.",
                "We have partially or informally considered verification methods to measure and ensure different aspects of the system's reliability and reproducibility, but specific details on our approach may not be available at this time.",
                "We have not put in place specific verification methods to measure and ensure aspects of the system's reliability and reproducibility.",
                "We consider that implementing verification methods for reliability and reproducibility is not applicable to our specific AI system or use case. "]
            q26 = st.radio("", q26_options)

            selected_index = q26_options.index(q26)
            answers_dict[category][0] += 2
        
        
        # Question 27
        st.markdown("##### Did you put in place processes to describe when an AI system fails in certain types of settings?")
        q27_options = [
            "We have established processes to comprehensively describe when our AI system fails in specific types of settings. We can provide detailed information on our failure reporting and documentation procedures. ",
            "We have partially or informally considered processes to describe AI system failures in certain types of settings, but specific details on our approach may not be available at this time.",
            "We have not implemented specific processes to describe when our AI system fails in particular types of settings. ",
            "We consider that establishing processes for describing AI system failures in specific settings is not applicable to our specific AI system or use case."]
        q27 = st.radio("", q27_options)

        selected_index = q27_options.index(q27)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 28
            st.markdown("##### Did you clearly document and operationalise these processes for the testing and verification of the reliability of AI systems?")
            q28_options = [
                "We have clearly documented and operationalized processes for the testing and verification of the reliability of our AI systems. We can provide detailed information on our documentation and operationalization procedures.",
                "We have partially or informally documented and operationalized processes for testing and verifying the reliability of our AI systems, but specific details on our approach may not be available at this time.",
                "We have not specifically documented and operationalized processes for testing and verifying the reliability of our AI systems.",
                "We consider that documenting and operationalizing processes for testing and verifying reliability is not applicable to our specific AI system or use case. "]
            q28 = st.radio("", q28_options)

            selected_index = q28_options.index(q28)
            update_dict(selected_index, category)
        
        
        # Question 29
        st.markdown("##### Did you establish mechanisms of communication to assure (end-)users of the system’s reliability?")
        q29_options = [
            "We have established robust mechanisms of communication to assure end-users of the reliability of our AI system. We can provide detailed information on our communication strategies and mechanisms.",
            "We have partially or informally established mechanisms of communication to assure end-users of the reliability of our AI system, but specific details on our approach may not be available at this time.",
            "We have not established specific mechanisms of communication to assure end-users of the reliability of our AI system.",
            "We consider that establishing mechanisms of communication for assuring end-users of reliability is not applicable to our specific AI system or use case."]
        q29 = st.radio("", q29_options)

        selected_index = q29_options.index(q29)
        update_dict(selected_index, category)
        
        st.markdown("## SECTION 3: PRIVACY AND DATA GOVERNANCE")
        st.markdown("### RESPECT FOR PRIVACY AND DATA PROTECTION")
        category = "Respect for Privacy and Data Protection"
        # Question 30
        st.markdown("##### Considering this use case, did you establish a mechanism allowing others to flag issues related to privacy or data protection in the AI system’s processes of data collection (for training and operation) and data processing?")
        q30_options = [
            "We have established a robust mechanism allowing others to flag issues related to privacy or data protection in the AI system's processes of data collection (for training and operation) and data processing. We can provide detailed information on our mechanisms for issue reporting and resolution.",
            "We have partially or informally established a mechanism for others to flag issues related to privacy or data protection in the AI system's processes, but specific details on our approach may not be available at this time.",
            "We have not specifically established a mechanism for others to flag issues related to privacy or data protection in the AI system's processes of data collection and processing.",
            "We consider that establishing a mechanism for flagging privacy or data protection issues is not applicable to our specific AI system or use case."]
        q30 = st.radio("", q30_options)

        selected_index = q30_options.index(q30)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 31
            st.markdown("##### Did you take measures to enhance privacy, such as via encryption, anonymisation and aggregation?")
            q31_options = [
                "We have implemented comprehensive measures to enhance privacy, incorporating encryption, anonymization, and aggregation techniques in our AI system. We can provide detailed insights into our privacy-enhancing methodologies.",
                "We have partially or informally taken measures to enhance privacy, including elements of encryption, anonymization, and aggregation, but specific details on our approach may not be available at this time.",
                "We have not specifically taken measures to enhance privacy through encryption, anonymization, or aggregation in our AI system.",
                "We consider that implementing measures to enhance privacy, such as encryption, anonymization, or aggregation, is not applicable to our specific AI system or use case."]
            q31 = st.radio("", q31_options)

            selected_index = q31_options.index(q31)
            update_dict(selected_index, category)

        
        # Question 32
        st.markdown("##### Did you assess the type and scope of data in your data sets (for example whether they contain personal data)?")
        q32_options = [
            "We have conducted a thorough assessment of the type and scope of data in our datasets, including determining whether they contain personal data. We can provide detailed information on our data assessment methodologies.",
            "We have partially or informally assessed the type and scope of data in our datasets, including considering whether they contain personal data, but specific details on our approach may not be available at this time.",
            "We have not specifically assessed the type and scope of data in our datasets, including whether they contain personal data.",
            "We consider that assessing the type and scope of data, including whether it contains personal data, is not applicable to our specific AI system or use case."]
        q32 = st.radio("", q32_options)

        selected_index = q32_options.index(q32)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 33
            st.markdown("##### Did you consider ways to develop the AI system or train the model without or with minimal use of potentially sensitive or personal data?")
            q33_options = [
                "We have actively considered and implemented ways to develop the AI system or train the model without or with minimal use of potentially sensitive or personal data. We can provide detailed insights into our approaches for minimizing data sensitivity.",
                "We have partially or informally considered ways to develop the AI system or train the model with minimal use of potentially sensitive or personal data, but specific details on our approach may not be available at this time.",
                "We have not specifically considered ways to develop the AI system or train the model without or with minimal use of potentially sensitive or personal data.",
                "Ways to develop the AI system or train the model with minimal use of potentially sensitive or personal data is not applicable to our specific AI system or use case. "]
            q33 = st.radio("", q33_options)

            selected_index = q33_options.index(q33)
            update_dict(selected_index, category)

        
        # Question 34
        st.markdown("##### Did you build in mechanisms for notice and control over personal data in this use case (such as valid consent and possibility to revoke, when applicable)?")
        q34_options = [
            "We have incorporated robust mechanisms for notice and control over personal data in this use case, including provisions for valid consent and the ability to revoke consent when applicable. We can provide detailed information on our mechanisms for data notice and control.",
            "We have partially or informally built in mechanisms for notice and control over personal data in this use case, including elements of valid consent and revocation options, but specific details on our approach may not be available at this time.",
            "We have not specifically built in mechanisms for notice and control over personal data in this use case, such as valid consent and the ability to revoke consent.",
            "We consider that building in mechanisms for notice and control over personal data is not applicable to our specific AI system or use case."]
        q34 = st.radio("", q34_options)

        selected_index = q34_options.index(q34)
        update_dict(selected_index, category)

        # Question 35
        st.markdown("##### Did you put in place processes to ensure the quality and integrity of your data?")
        q35_options = [
            "We have implemented robust processes to ensure the quality and integrity of our data. We can provide detailed information on our data quality assurance and integrity verification methodologies.",
            "We have partially or informally put in place processes to ensure the quality and integrity of our data, but specific details on our approach may not be available at this time.",
            "We have not specifically put in place processes to ensure the quality and integrity of our data.",
            "We consider that putting in place processes to ensure the quality and integrity of data is not applicable to our specific AI system or use case. "]
        q35 = st.radio("", q35_options)

        selected_index = q35_options.index(q35)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 36
            st.markdown("##### How are you verifying that your data sets have not been compromised or hacked?")
            q36_options = [
                "We have implemented comprehensive mechanisms to verify that our datasets have not been compromised or hacked. We can provide detailed information on our data security verification procedures, including encryption and intrusion detection measures.",
                "We have partially or informally implemented mechanisms to verify that our datasets have not been compromised or hacked, but specific details on our approach may not be available at this time.",
                "We have not specifically implemented mechanisms to verify that our datasets have not been compromised or hacked.",
                "We consider that verifying datasets for compromise or hacking is not applicable to our specific AI system or use case."]
            q36 = st.radio("", q36_options)

            selected_index = q36_options.index(q36)
            update_dict(selected_index, category)
        
        st.markdown("### ACCESS TO DATA")
        category = "Access to Data"
        # Question 37
        st.markdown("##### Did you assess who can access users’ data, and under what circumstances?")
        q37_options = [
            "We have conducted a thorough assessment of who can access users' data and under what circumstances. We can provide detailed insights into our access control mechanisms and the criteria governing data access.",
            "We have partially or informally assessed who can access users' data and under what circumstances, but specific details on our approach may not be available at this time.",
            "We have not specifically assessed who can access users' data and under what circumstances.",
            "We consider that assessing who can access users' data and under what circumstances is not applicable to our specific AI system or use case."]
        q37 = st.radio("", q37_options)

        selected_index = q37_options.index(q37)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 38
            st.markdown("##### Did you ensure that these persons are qualified and required to access the data, and that they have the necessary competences to understand the details of data protection policy?")
            q38_options = [
                "We have ensured that individuals with access to users' data are qualified, required to access the data, and possess the necessary competences to understand the details of our data protection policy. We can provide detailed information on our qualification verification processes and training programs.",
                "We have partially or informally ensured that individuals with access to users' data are qualified, required to access the data, and possess the necessary competences to understand our data protection policy, but specific details on our approach may not be available at this time.",
                "We have not specifically ensured that individuals with access to users' data are qualified, required to access the data, and possess the necessary competences to understand the details of our data protection policy.",
                "We consider that ensuring the qualifications and competences of individuals accessing users' data is not applicable to our specific AI system or use case."]
            q38 = st.radio("", q38_options)

            selected_index = q38_options.index(q38)
            update_dict(selected_index, category)

        # Question 39
        st.markdown("##### Did you ensure an oversight mechanism to log when, where, how, by whom and for what purpose data was accessed?")
        q39_options = [
            "We have implemented a comprehensive oversight mechanism to log when, where, how, by whom, and for what purpose data was accessed. We can provide detailed information on our data access logging procedures and oversight mechanisms.",
            "We have partially or informally ensured an oversight mechanism to log data access details, but specific details on our approach may not be available at this time.",
            "We have not specifically ensured an oversight mechanism to log when, where, how, by whom, and for what purpose data was accessed.",
            "We consider that ensuring an oversight mechanism for data access logging is not applicable to our specific AI system or use case."]
        q39 = st.radio("", q39_options)

        selected_index = q39_options.index(q39)
        update_dict(selected_index, category)

        st.markdown("### TRANSPARENCY")
        category = "Transparency"
        # Question 40
        st.markdown("##### Does your model encompass transparency in regards to its traceability, explainability, and open communication?")
        q40_options = [
            "We have implemented mechanisms that ensure traceability and explainability of the decisions, explainability of the data, processes, and decisions and communicate these and the purpose of the model to the end-users",
            "We have implemented only some mechanisms that ensure traceability and explainability of the decisions, explainability of the data, processes, and decisions and occasionally communicate to the end-users",
            "We have not implemented traceability and explainability of the model as well as  do not communication with users",
            "These issues are not applicable to our case"]
        q40 = st.radio("", q40_options)

        selected_index = q40_options.index(q40)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)

        if answers.pop() == 1 or answers.pop() == 0:
            # Question 41
            st.markdown("#### *Traceability*")
            st.markdown("##### Did you put in place measures that address the traceability of the AI system during its entire lifecycle aimed to enhance transparency and achieve trustworthy AI?")
            q41_options = [
                "We have implemented mechanisms that allow for full traceability from the input data to the output, provide documentation of  data and processes  leading to decisions",
                "We have some mechanisms that only trace parts of the AI system lifecycle and provide documentation for the traceable parts",
                "We have not implemented traceability, explainability, and effective communication with users",
                "We consider that these issues are not applicable to our case"]
            q41 = st.radio("", q41_options)

            selected_index = q41_options.index(q41)
            update_dict(selected_index, category)

            # Question 42
            st.markdown("#### *Explainability*")
            st.markdown("##### Can your model explain its decisions and its outputs to the users?")
            q42_options = [
                "We have a model that explains both the technical processes of the AI system and the reasoning behind the decisions or predictions that the AI system makes. An explanation is provided regarding why the model has generated a particular output or decision, including the combination of input factors that contributed to it",
                "We have a model that is unable to explain the process or the decision adequately,   black boxes may hinder explainability",
                "We have a model that cannot explain the output nor the process to reach a decision or provides little explainability, even though erroneous outputs can greatly impact human life",
                "We consider that these issues are not applicable to our case"]
            q42 = st.radio("", q42_options)

            selected_index = q42_options.index(q42)
            update_dict(selected_index, category)

            # Question 43
            st.markdown("#### *Communication*")
            st.markdown("##### Do you communicate to users that they are interacting with an AI system instead of a human?")
            q43_options = [
                "We inform end-users that they are interacting with an AI system instead of a human every time the system is in use",
                "We only inform end-users when they are using an interactive AI system or in scenarios with high risk",
                "No, we do not inform end-users when they are using AI ",
                "We consider that these issues are not applicable to our case"]
            q43 = st.radio("", q43_options)

            selected_index = q43_options.index(q43)
            update_dict(selected_index, category)

        # Question 44
        st.markdown("##### Do you outline your model’s purpose, benefits, limitations, and risks comprehensively before users engage with it?")
        q44_options = [
            "Yes, we provide a detailed outline of benefits, limitations, and risks the model poses as well as information detailing how to use the AI system",
            "We only provides a general overview of benefits and/or limitations and/or risks the model poses",
            "We do not provide any information explaining the model",
            "We consider that these issues are not applicable to our case"]
        q44 = st.radio("", q44_options)

        selected_index = q44_options.index(q44)
        update_dict(selected_index, category)

        st.markdown("### DIVERSITY, NON-DISCRIMINATION, AND FAIRNESS")
        category = "Diversity, Non-discrimination and Fairness"
        # Question 45
        st.markdown("##### Do you address potential unfair bias and  accessibility?")
        q45_options = [
            "Our system includes both inclusion and diversity standards to enforce Trustworthy AI in both the training and operation stages",
            "Our system only includes inclusion and/or diversity standards in the training stage of the model",
            "Our system does not include inclusion and/or diversity standards any stage of the model",
            "We consider that these issues are not applicable to our case"]
        q45 = st.radio("", q45_options)

        selected_index = q45_options.index(q45)
        answers.append(2)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)
        update_dict(selected_index, category)
        
        if answers.pop() == 1 or answers.pop() == 0:
            # Question 45
            st.markdown("##### Does your system implement strategies to ensure that fairness and diversity is implemented into your system?")
            q45_options = [
                "Our system has implemented strategies to ensure fairness and diversity in the use of input data and algorithm design  and has procedures to check for errors related to bias and discrimination",
                "Our system has implemented strategies to ensure fairness and diversity in input data or algorithm design but does not contain procedures to check for errors",
                "Our system has not implemented strategies to ensure fairness and diversity",
                "We consider that these issues are not applicable to our case"]
            q45 = st.radio("", q45_options)

            selected_index = q45_options.index(q45)
            update_dict(selected_index, category)

        # Question 46
        st.markdown("##### Did you perform research to define fairness and understand the diversity of end-users?")
        q46_options = [
            "We researched types of bias, diversity and representativeness of end-users,  subjects in the data, and researched and included widely-accepted definitions of fairness, consult with various communities",
            "We only researched definition of fairness and the diversity of end-users",
            "We did not perform any research nor educated AI designers and developers",
            "We consider that these issues are not applicable to our case"]
        q46 = st.radio("", q46_options)

        selected_index = q46_options.index(q46)
        update_dict(selected_index, category)

        # Question 47
        st.markdown("##### Is your system’s outputs fair to disproportionate communities?")
        q47_options = [
            "Our system flags output issues related to bias, identifies potential communities that could be affected by the AI system, contain a quantitative analysis that measures the inclusion of fairness",
            "Our system does not have multiple mechanisms and/or analysis to ensure fairness",
            "Our system does not contain any mechanisms and analysis to ensure fairness",
            "We consider that these issues are not applicable to our case"]
        q47 = st.radio("", q47_options)

        selected_index = q47_options.index(q47)
        update_dict(selected_index, category)

        # Question 48
        st.markdown("##### Is your system inclusive for any population that exhibits different levels of  abilities?")
        q48_options = [
            "Our system addressed different preferences of end-users, has an interface that uses Universal Design or an interface that is accessible to those with special needs, disabilities, and more",
            "Our system only has addressed preferences and interface design that is usable by only a small number of minorities",
            "Our system does not address preferences or interface design of those with different accessibility and preference needs",
            "We consider that these issues are not applicable to our case"]
        q48 = st.radio("", q48_options)

        selected_index = q48_options.index(q48)
        update_dict(selected_index, category)

        st.markdown("### SOCIETAL AND ENVIRONMENTAL WELLBEING")
        category = "Societal and Environmental Wellbeing"
        # Question 49
        st.markdown("##### Does the system contain features that combat environmental concerns due to the amount of energy it uses and potentially increasing carbon emissions?")
        q49_options = [
            "The system has implemented mechanisms that identifies, tracks and recommends methods to reduce amount of energy used and carbon emissions throughout the AI system’s life cycle",
            "The system has only identified and/or tracks the amount of energy used and carbon emissions throughout parts of the AI system cycle",
            "The system has not implemented any measures to ensure environmental well being",
            "We consider that these issues are not applicable to our case"]
        q49 = st.radio("", q49_options)

        selected_index = q49_options.index(q49)
        update_dict(selected_index, category)

        # Question 50
        st.markdown("##### Does the system increase risks that will disrupt the workforce and work arrangements?")
        q50_options = [
            "The system assesses the risk it may pose to workers, the relationship between workers and employers, and on skills. It also strives to supplement the workforce in certain tasks and ensures workers understand the purpose and operation of the system",
            "The system only provides quantitative reports that identify the risk it may pose to workers, the relationship between workers and employers, and on skills",
            "The AI system creates the risk of eliminating the working force in specific industries and has no plans to support human workers",
            "We consider that these issues are not applicable to our case"]
        q50 = st.radio("", q50_options)

        selected_index = q50_options.index(q50)
        update_dict(selected_index, category)

        st.markdown("### ACCOUNTABILITY")
        category = "Accountability"
        # Question 51
        st.markdown("##### Does the system have proper mechanisms to allow for accountability with the system through investigations by both internal and third-party committees and allows for redressing?")
        q51_options = [
            "We have established mechanisms that facilitate the AI system’s auditability, risk identification, risk management, and transparency by both internal and third-party committees. We also have the ability to redress mechanisms",
            "We only have established mechanisms that facilitate the AI system’s auditability by internal and/or third-party committees",
            "We do not have established mechanisms and the ability to redress certain issues",
            "We consider that these issues are not applicable to our case"]
        q51 = st.radio("", q51_options)

        selected_index = q51_options.index(q51)
        update_dict(selected_index, category)

        submit_button = st.button("Submit")
        if submit_button:
            def to_csv(df):
                # Convert DataFrame to CSV and then encode it
                output = BytesIO()
                df.to_csv(output, index=False)  # Index=False means that the row indices will not be written
                processed_data = output.getvalue().decode("utf-8")
                return processed_data
            
            for key in answers_dict:
                answers_dict[key] = answers_dict[key][0] / answers_dict[key][1]
            df = pd.DataFrame([answers_dict])
            df['Timestamp'] = datetime.now().strftime('%m/%d/%Y')
            if previous_data is not None:
                st.session_state['combined_data'] = pd.concat([previous_data, df], ignore_index=True)
            else:
                st.session_state['combined_data'] = df

            st.plotly_chart(plot_spider_chart(st.session_state['combined_data']))
            # st.write(st.session_state['combined_data'])
            # Convert DataFrame to CSV
            csv = st.session_state['combined_data'].to_csv(index=False).encode('utf-8')
            

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='report.csv',
                mime='text/csv',
            )
        
    if st.session_state['generate_report_initiated']:
        st.write("Please only submit a CSV from a previous questionnaire result or the system will not produce a report")
        files = ask_for_csv()  # This should return a DataFrame
        if files is not None:
            st.plotly_chart(plot_spider_chart(files))
            csv = st.session_state['combined_data'].to_csv(index=False).encode('utf-8')
            

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='report.csv',
                mime='text/csv',
            )
            

# Run the app
if __name__ == "__main__":
    main()