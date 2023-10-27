# Import Streamlit library
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    st.title("AI Guidelines Questionnaire for Companies")

    # Create a list to store answers
    answers = []

    # Question 1
    st.markdown("### 1.Inform on how it is respecting fundamental rights of individuals:")
    st.markdown("""##### How are you dealing with the effect of the application on the rights to safety, health, non-discrimination, and freedom of association?""")
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
    else:
        answers.append(0)

    # Question 2
    st.markdown("### 2. Privacy and data protection:")
    st.markdown("##### Is data collection compliant with the General Data Protection Regulation (GDPR) and does it respect the privacy of the users?")
    st.markdown("*Note: A Data Protection Impact Assessment (DPIA) must be carried out before deploying any system.*")
    q2_options = ["""The purpose of the AI system and the mechanisms to assess its usage are clearly defined and compliant with GDPR, a DPIA 
                  has been performed and privacy of individuals is guaranteed. We can provide further information.""", 
                  """We have only done a partial/informal analysis and/or not all aspects of data and privacy protection are clear.""", 
                  """We cannot guarantee privacy and data protection.""",
                  """We cannot guarantee privacy and data protection."""]  
    q2 = st.radio("", q2_options)

    selected_index = q2_options.index(q2)

    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    st.write("\n")  

    # Question 3
    st.markdown("### 3. Transparency rights:")
    st.markdown("##### Do you include the right of users to:")
    st.markdown("- ###### be notified that their data is being processed/collected,")
    st.markdown("- ###### access information on which personal data are collected,")
    st.markdown("- ###### control their own data,")
    st.markdown("- ###### access explanations of results produced by the system,")
    st.markdown("- ###### be informed of who, when, and how the system can be audited.")

    q3_options = [
           "All of the above are fulfilled.",
           "Only some of the above are fulfilled or partially addressed.",
           "We cannot guarantee any transparency aspects.",
           "We consider that these issues are not applicable to our case."]
    q3 = st.radio("", q3_options)

    selected_index = q3_options.index(q3)

    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 4
    st.markdown("### 4. Accessibility:")
    st.markdown("##### Can your app/system/resource be used by all regardless of demographics, language, disability, digital literacy, and financial accessibility?")
    q4_options = [
        "This resource is fully accessible, and we can provide information on accessibility accommodations.",
        "This resource partially complies with accessibility requirements.",
        "This resource is not accessible to all.",
        "We consider that these issues are not applicable to our case."
    ]
    q4 = st.radio("", q4_options)

    selected_index = q4_options.index(q4)

    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 5
    st.markdown("### 5. Education and tutorials:")
    st.markdown("##### Do you ensure that users are informed and capable of using the system correctly?")
    q5_options = [
        "We provide complete in-system help.",
        "We provide support through external materials, e.g. website.",
        "We do not provide user support.",
        "We consider that these issues are not applicable to our case."
    ]
    q5 = st.radio("", q5_options)

    selected_index = q5_options.index(q5)

    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Technology
    # Question 6
    st.markdown("### 6. Data management:")
    st.markdown("##### Do you comply with the data-minimization principle, i.e. usage of local and temporary storage and encryption, based on principles of data protection by design? Do you ensure that only strictly necessary data are captured and processed?")
    q6_options = [
        "We use local and temporary storage and data encryption methods. We only collect and process strictly necessary data. We can provide further information.",
        "We partially comply with the above, and some documentation can be provided.",
        "We do not comply with these data management aspects.",
        "We consider that these issues are not applicable to our case."]
    q6 = st.radio("", q6_options)

    selected_index = q6_options.index(q6)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 7
    st.markdown("### 7. Security:")
    st.markdown("##### Do you have user authentication in place to prevent risks such as access, modification, or disclosure of the data? Do you use unique and pseudo-random identifiers, renewed regularly and cryptographically strong?")
    q7_options = [
        "Strong security elements are in place, e.g. user authentication, unique identifiers regularly renewed. We can provide further information.",
        "Some security features are in place.",
        "No security features are in place.",
        "We consider that these issues are not applicable to our case."]
    q7 = st.radio("", q7_options)

    selected_index = q7_options.index(q7)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 8
    st.markdown("### 8. Ease to deactivate/remove:")
    st.markdown("##### How easy is it to deactivate or remove the system and data once users are no longer interested or need the system?")
    q8_options = [
        "Very easy, either through clear instructions or automatically by the sunset clause.",
        "Instructions on how to deactivate or remove the system and data are unclear.",
        "There are no instructions or automated procedures to remove the system and the data.",
        "We consider that these issues are not applicable to our case."]
    q8 = st.radio("", q8_options)

    selected_index = q8_options.index(q8)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 9
    st.markdown("### 9. Ease to access services without using the AI system:")
    st.markdown("##### In the case of AI systems aimed to replace or complement public services, are there full non-system alternatives?")
    q9_options = [
        "Yes, there is an easily accessible full non-system alternative.",
        "There is a partial alternative or access to the full alternative is unclear.",
        "There is no alternative to the AI system for this service.",
        "We consider that these issues are not applicable to our case."]
    q9 = st.radio("", q9_options)

    selected_index = q9_options.index(q9)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 10
    st.markdown("### 10. Open-source code:")
    st.markdown("##### Is the development participatory and multidisciplinary? What kind of access to the code and development is there?")
    q10_options = [
        "The code and development are open-source.",
        "The code is open-source code without the possibility of contributing.",
        "Non-open-source code.",
        "We consider that these issues are not applicable to our case."]
    q10 = st.radio("", q10_options)

    selected_index = q10_options.index(q10)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 11: Ownership
    st.markdown("### 11. Ownership:")
    st.markdown("##### Is the ownership of the resource clear?")
    q11_options = [
        "Ownership of the resource (including code, data, use) is clear and explicit.",
        "Some ownership aspects are made clear.",
        "Ownership information for the resource and related code or data is unavailable.",
        "We consider that these issues are not applicable to our case."]
    q11 = st.radio("", q11_options)

    selected_index = q11_options.index(q11)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 12: Openness over Data governance
    st.markdown("### 12. Openness over Data governance:")
    st.markdown("##### How open is Data governance?")
    q12_options = [
        "Open data governance.",
        "Intermediate openness of data governance.",
        "Private/opaque settings.",
        "We consider that these issues are not applicable to our case."]
    q12 = st.radio("", q12_options)

    selected_index = q12_options.index(q12)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

    # Question 13: Legislation and Policy
    st.markdown("### 13. Legislation and Policy:")
    st.markdown("##### Are there explicit legislation and/or other policies relevant to your system/resource?")
    q13_options = [
        "The system is covered by an explicit clear, legal framework or sectorial formal policies, and we address these explicitly.",
        "We are aware of policy partially relevant to our system and address these sufficiently.",
        "We are not aware of any relevant legislation or policy and do not address these.",
        "We consider that these issues are not applicable to our case."]
    q13 = st.radio("", q13_options)

    selected_index = q13_options.index(q13)
    if selected_index == 0:
        answers.append(2)
    elif selected_index == 1:
        answers.append(1)
    else:
        answers.append(0)

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
        df = load_df(answers)
        st.plotly_chart(plot_spider_chart(df))

# Run the app
if __name__ == "__main__":
    main()