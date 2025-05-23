import streamlit as st
from .dl_states import Token
import os

def apply_custom_css():
    custom_css = """
    <style>
        .question-style {
            font-size: 20px; /* Customize the font size as needed */
            font-weight: bold; /* Optional: Make the question bold */
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def question_generator(label, options, question_key):
    question = st.radio(label='Please select the correct answer', options=options, key=question_key)
    return question

def sa_questions():
    apply_custom_css()

    # Initialize token and questions only once
    if 'token' not in st.session_state:
        st.session_state.token = None
        st.session_state.questions_initialized = False

    st.markdown("### Please select a topic to proceed:")
    
    # Use the lesson names from the provided image
    initial_options = {
        "Lesson 1: Linear Classifiers and Gradient Descent": '1', 
        "Lesson 2: Neural Networks": '2',
        "Lesson 3: Optimization of Deep Neural Networks": '3',
        "Lesson 4: Data Wrangling": '4',
        "Lesson 5: Convolution and Pooling Layers": '5',
        "Lesson 6: Convolutional Neural Networks": '6',
        "Lesson 7: Visualization": '7',
        "Lesson 9: Advanced Computer Vision and Applications": '9',
        "Lesson 10: Responsible AI and Bias and Fairness": '10',
        "Lesson 11: Introduction to Structured Data": '11',
        "Lesson 12: Language Models": '12',
        "Lesson 13: Embeddings": '13',
        "Lesson 14: Neural Attention Models": '14',
        "Lesson 15: Neural Machine Translation and COMPUTATION": '15',
        "Lesson 17: Deep Reinforcement Learning": '17',
        "Lesson 18: Unsupervised and Semi-Supervised Learning": '18',
        "Lesson 19: Generative Models": '19'
    }
    
    topics = {
        "Lesson 1: Linear Classifiers and Gradient Descent": '1',
        "Lesson 2: Neural Networks": '2',
        "Lesson 3: Optimization of Deep Neural Networks": '3',
        "Lesson 4: Data Wrangling": '4',
        "Lesson 5: Convolution and Pooling Layers": '5',
        "Lesson 6: Convolutional Neural Networks": '6',
        "Lesson 7: Visualization": '7',
        "Lesson 8: Scalable Training": '8',
        "Lesson 9: Advanced Computer Vision and Applications": '9',
        "Lesson 10: Responsible AI and Bias and Fairness": '10',
        "Lesson 11: Introduction to Structured Data": '11',
        "Lesson 12: Language Models": '12',
        "Lesson 13: Embeddings": '13',
        "Lesson 14: Neural Attention Models": '14',
        "Lesson 15: Neural Machine Translation": '15',
        "Lesson 16: Advanced Topics: Translation": '16',
        "Lesson 17: Deep Reinforcement Learning": '17',
        "Lesson 18: Unsupervised and Semi-Supervised Learning": '18',
        "Lesson 19: Generative Models": '19'
    }
    
    selected_option = st.radio(label=' ', options=list(initial_options.keys()), label_visibility="collapsed")

    if st.button("Proceed") or st.session_state.questions_initialized:
        if not st.session_state.questions_initialized:
            st.session_state.STATE = initial_options[selected_option]
            st.session_state.token = Token(STATE=st.session_state.STATE)
            st.session_state.token.initialize_mpc_questions()
            st.session_state.questions = st.session_state.token.mpc_questions
            st.session_state.questions_initialized = True

        questions = st.session_state.questions
        for i, q in enumerate(questions, start=0):
            label = q['question']
            options = q['options_list']
            # Correct answer handling
            correct_answer = q['correct_answer']
            
            explanation = q.get('explanation', " ")

                
            # If the correct answer is 'True' or 'False', keep it as it is
            if correct_answer in ['True', 'False']:
                correct_answer = correct_answer
            
            # If the correct answer is a single letter ('A', 'B', 'C', or 'D'), convert it to the corresponding option
            elif correct_answer[0] in ['A', 'B', 'C', 'D'] and len(correct_answer) == 1:
                correct_answer_letter = correct_answer
                correct_answer = options[ord(correct_answer_letter) - ord('A')]
            question_key = f"question_{i}"
            # explanation = q['explanation']

            st.markdown('-------------------------------')
            # Directly use st.markdown for the question text, allowing LaTeX to render
            st.markdown(f"**{label}**")

            question = question_generator(label, options, question_key)
            
            image_dir = os.path.join(os.getcwd(), 'CS_7643_Deep_Learning/')
            if 'image' in q and q['image']:
                # print('current dir:', print(os.getcwd()))
                image_path = os.path.join(image_dir, q['image'])
                st.write(f"Current working directory: {os.getcwd()}")

                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                else:
                    st.write("Image not found.")
                
            if st.button('Submit', key=f"submit_{i}"):
                if question == correct_answer:
                    st.success('Great work!')
                    st.info(f'Explanation: \n\n{explanation}')
                else:
                    st.error(f"The correct answer was {correct_answer}")
                    st.info(f'Explanation: \n\n{explanation}')

                if 'chapter_information' in q:
                    st.write(f"You can review {q['chapter_information']}")
            


if __name__ == "__main__":
    sa_questions()
