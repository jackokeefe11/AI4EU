# Import Streamlit library
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from dateutil.parser import parse
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

    
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

combined_df = pd.DataFrame()
def ask_for_csv():
    global combined_df
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        if uploaded_file.name[-3:] != "csv":
            st.write("Only csv files are accepted")
            continue  # Use continue to skip to the next file

        dataframe = pd.read_csv(uploaded_file)
        if dataframe.columns[1:].tolist() != ['Impact', 'Technology', 'Governance']:
            st.write("Only prior csv files from this application are accepted")
            continue

        last_row = dataframe.iloc[-1]
        if pd.to_datetime(last_row, errors='coerce').nunique() != 1:
            st.write("Only prior csv files from this application are accepted")
            continue

        # Concatenate valid DataFrame
        combined_df = pd.concat([combined_df, dataframe], ignore_index=False)

    return combined_df

# Create a dataframe to store answers
def load_df(answers):
    columns = ['Impact', 'Technology', 'Governance']
    index = []

    for i in range(15):
        if i < 5:
            index.append('Impact Q' + str(i+1))
        elif i < 10:
            index.append('Technology Q' + str(i+1))
        else:
            index.append('Governance Q' + str(i+1))
    index.append('Date')

    df = pd.DataFrame(columns=columns, 
                    index=index)
    
    # Initialize to all 0's
    df.iloc[:, :] = 0
    
    for i in range(15):
        if i < 5:
            df.iloc[i, 0] = answers[i]
        elif i < 10:
            df.iloc[i, 1] = answers[i]
        else:
            df.iloc[i, 2] = answers[i]

    df = df[~(df == -1).any(axis=1)]

    df.loc['Date'] = date.today()
    print(df)
    return df

# Plot the spider Plot 
def plot_spider_chart(df):
    categories = df.index.tolist()

    # Create a figure
    fig = go.Figure()

    # Adding traces for each column in df
    for col in df.columns:
        fig.add_trace(go.Scatterpolar(
            r=df[col].tolist(),
            theta=categories,
            fill='toself',
            name=col
        ))
    
    fig.update_yaxes(title_font_color="black")
    return fig

# Inject the CSS to change the circle color
def load_custom_css(css_path):
    with open(css_path, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the custom CSS
load_custom_css('styles.css')

# Main app
def main():
    if 'update_report_initiated' not in st.session_state:
        st.session_state['update_report_initiated'] = False
    if 'generate_report_initiated' not in st.session_state:
        st.session_state['generate_report_initiated'] = False
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False
    if 'df_download' not in st.session_state:  # Initialize 'df_download' in session state
        st.session_state['df_download'] = pd.DataFrame()  # Assuming pd is pandas
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

    if st.session_state['update_report_initiated'] and not st.session_state['submitted']:
        ask_for_csv()
                    
        # Create a list to store answers
        answers = []
        answers_short = []

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

        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Question 2
        st.markdown("### EDUCATION AND TUTORIALS")
        st.markdown("##### Are the end users or subjects informed that they are interacting with an AI system and that a decision,content, advice or outcome is a result of an algorithmic decision?")
        q2_options = ["""Users are aware of both.""", 
                    """Users are aware that they are interacting with an AI system, but aren’t aware of how the system comes to a final answer. """, 
                    """We have not considered these issues yet.""",
                    """We consider that these issues are not applicable to our case."""]  
        q2 = st.radio("", q2_options)

        selected_index = q2_options.index(q2)

        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Question 3
        st.markdown("### HUMAN AUTONOMY")
        st.markdown("##### Could the AI system affect human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way?")

        q3_options = [
            "Yes, the system affects human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way.",
            "The system might affect human autonomy by interfering with the end-user’s decision-making process in any other unintended and undesirable way.",
            "We have not considered these issues yet. ",
            "We consider that these issues are not applicable to our case. "]
        q3 = st.radio("", q3_options)

        selected_index = q3_options.index(q3)

        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Question 4
        st.markdown("##### Was any procedure put in place to avoid that the AI system inadvertently affects human autonomy?")
        q4_options = [
            "Yes, it a procedure was put in place to avoid that the AI system inadvertently affects human autonomy",
            "No procedure was put in place",
            "We have not considered these issues yet.",
            "We consider that these issues are not applicable to our case. "
        ]
        q4 = st.radio("", q4_options)

        selected_index = q4_options.index(q4)

        if selected_index == 0:
            answers_short.append(2)
        elif selected_index == 1:
            answers_short.append(1)
        elif selected_index == 2:
            answers_short.append(0)
        else:
            answers_short.append(-1)

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

        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Technology
        # Question 6
        st.markdown("### HUMAN OVERSIGHT")
        st.markdown("##### How easy is it to deactivate/abort an operation while needed or remove the system and data once users are no longer interested or need the system?")
        q6_options = [
            "Very easy, either through clear instructions or automatically by a sunset clause.",
            "Instructions on how to deactivate or remove the system and data are unclear. ",
            "We have not considered these issues yet",
            "We consider that these issues are not applicable to our case."]
        q6 = st.radio("", q6_options)

        selected_index = q6_options.index(q6)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        st.markdown("### GOVERNANCE MECHANISMS")
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
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

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
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

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
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

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
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Section 2
        st.markdown("## SECTION 2: TECHNICAL ROBUSTNESS AND SAFETY")
        st.markdown("### RESILIENCE TO ATTACK AND SECURITY")
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
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        elif selected_index == 2:
            answers.append(0)
        else:
            answers.append(-1)

        # Question 12: Cybersecurity Certification of AI System
        st.markdown("##### Is the AI system certified for cybersecurity (e.g the certification scheme created by the Cybersecurity Act in Europe) or is it compliant with specific security standards?")
        q12_options = [
            "The AI system is certified for cybersecurity. (2)",
            "The AI system is not certified for cybersecurity. (1)",
            "We consider that these issues are not applicable to our case. (N/A)"
        ]
        q12 = st.radio("", q12_options)
        selected_index = q12_options.index(q12)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        else:
            answers.append(-1)

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
            if selected_index == 0:
                answers.append(2)
            elif selected_index == 1:
                answers.append(1)
            elif selected_index == 2:
                answers.append(0)
            else:
                answers.append(-1)


        # Question 14: Design Impact Assessment and Open Development Process
        st.markdown("### 14. Design Impact Assessment and Open Development Process:")
        st.markdown("##### How explicit is the design process leading to this resource?")
        q14_options = [
            "Explicit information on the design process is available, including a clear description of aims and motivation, stakeholders, public consultation process and impact assessment.",
            "Some information on the design process, aims and motivation, and impact assessment is available.",
            "There is no information on the design and impact of the resource.",
            "We consider that these issues are not applicable to our case."]
        q14 = st.radio("", q14_options)

        selected_index = q14_options.index(q14)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        else:
            answers.append(0)

        # Question 15: Right to contest/liability
        st.markdown("### 15. Right to contest/liability:")
        st.markdown("##### Are users able to contest decisions/actions or demand human intervention?")
        q15_options = [
            "Processes for contesting and/or demanding human intervention are set up and clearly available.",
            "Some contestability or intervention processes are available.",
            "It is not possible to contest the system’s output nor to demand human intervention.",
            "We consider that these issues are not applicable to our case."]
        q15 = st.radio("", q15_options)

        selected_index = q15_options.index(q15)
        if selected_index == 0:
            answers.append(2)
        elif selected_index == 1:
            answers.append(1)
        else:
            answers.append(0)

        if st.button("Submit"):
            temp_df = load_df(answers)  # Process answers to create a DataFrame
            if not temp_df.empty:  # Ensure that the DataFrame is not empty
                st.session_state['df_download'] = temp_df
                st.write(print(temp_df))
                st.session_state['csv'] = convert_df(temp_df)  # Convert DataFrame to CSV
                st.session_state['submitted'] = True  # Set 'submitted' to True AFTER processing
            else:
                st.error("The uploaded data is invalid or empty.")

    # if st.session_state['submitted']:
    #     if not st.session_state['df_download'].empty:
    #         # Display the results after submission
    #         df_display = st.session_state['df_download']
    #         st.plotly_chart(plot_spider_chart(df_display))

    #         # Provide a download button for the CSV
    #         st.download_button(
    #             label="Download data as CSV",
    #             data=st.session_state['csv'],
    #             file_name='data.csv',
    #             mime='text/csv',
    #         )
    #     else:
    #         # If 'df_download' is empty, which shouldn't happen now, display an error message
    #         st.error("There was an error processing the data. The DataFrame is empty.")
        
    if 'generate_report_initiated' in st.session_state and st.session_state['generate_report_initiated']:
        st.write("Please only submit a CSV from a previous questionnaire result or the system will not produce a report")
        files = ask_for_csv()  # This should return a DataFrame
        def is_date_string(s):
            try:
                parse(s, fuzzy=False)
                return True
            except ValueError:
                return False

        def is_date_row(row):
            return all(row.apply(is_date_string))

        if files is not None and not files.empty:
            st.write(files)
            
            # Identifying the separator rows
            files_without_first = files.iloc[:, 1:]

            # Identifying the separator rows based on the adjusted DataFrame
            separator_indices = files_without_first.apply(is_date_row, axis=1)

            # Now separator_indices is a boolean series; to get the actual indices, use:
            separator_indices = separator_indices[separator_indices].index

            # Display the separator indices
            st.write(separator_indices)
            files.set_index(files.columns[0], inplace=True)

            # Splitting the DataFrame into sections
            sections = []
            start_idx = 0
            for end_idx in separator_indices:
                section = files.iloc[start_idx:end_idx]
                if not section.empty:
                    sections.append(section)
                start_idx = end_idx + 1
            if start_idx < len(files):
                sections.append(files.iloc[start_idx:])
            st.write(sections)

            for elem in sections:
                st.write(plot_spider_chart(elem))

            def create_progression_line_chart(sections):
                # Initialize a list to store the average values of each section
                section_averages = []

                # Calculate the average for each section after converting columns to integers
                for section in sections:
                    # Convert all columns to integers, handle NaN and non-numeric values by filling them with zeros
                    section_int = section.fillna(0).astype(int)
                    
                    # Sum all values in the section and divide by 30
                    section_sum = section_int.sum().sum()  # Summing all the values in the DataFrame
                    section_average = section_sum / 30
                    section_averages.append(section_average)

                # Create a new figure for the line chart
                fig, ax = plt.subplots(figsize=(10, 5))
                
                # Plot the line chart
                ax.plot(section_averages, marker='o')  # Using 'o' as a marker for each average point
                ax.set_title('Safety Measure Score Over Time')
                ax.set_xlabel('Report Number')
                ax.set_ylabel('Score (decimal))')
                ax.grid(True)
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                
                # Return the figure object
                return fig
            st.write(create_progression_line_chart(sections))
            

# Run the app
if __name__ == "__main__":
    main()