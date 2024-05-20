import streamlit as st
import base64
from PIL import Image

from visual_automata.fa.dfa import VisualDFA

r1 = "RegEx 1. (bab+bbb)b*a*(a*+b*)(ab)*(aba)(bab+aba)*bb(a+b)*(bab+aba)(a+b)*"
r2 = "RegEx 2. (1+0)*0*1*(111+00+101)(1+0)*(101+01+000)(1+0)*(101+000)*"

# Use the full page 
st.set_page_config(layout="wide")
st.title("Deterministic Finite Automaton (DFA) Simulator with Push Down Automata & Context-Free Grammar")

# Divide page by columns of equal size
c1, c2, c3, c4 = st.columns(4)

with c1:    
    st.subheader("① Choose a Regular Expression")
    user_choice = st.selectbox("", [r1, r2])

with c2:
    st.subheader("② Context-Free Grammar ")

st.markdown("---")    
st.markdown("## DFA Simulation")

# Display chosen RegEx
st.text(user_choice)

if user_choice == r1:
    dfa = VisualDFA(
        states={'0', '1', '2','3','4', '5', '6','7','8', '9', '10','11',
       '12', '13', '14','15'},
        input_symbols={"a", "b"},
        transitions={ '0' : {'a' : '13', 'b' : '1'},
            '1' : {'a' : '2', 'b' : '2'},
            '2' : {'a' : '14', 'b' : '3'},
            '3' : {'a' : '4', 'b' : '3'},
            '4' : {'a' : '4', 'b' : '5'},
            '5' : {'a' : '6', 'b' : '5'},
            '6' : {'a' : '6', 'b' : '7'},
            '7' : {'a' : '7', 'b' : '8'},
            '8' : {'a' : '9', 'b' : '11'},
            '9' : {'a' : '9', 'b' : '10'},
            '10' : {'a' : '15', 'b' : '11'},
            '11' : {'a' : '12', 'b' : '11'},
            '12' : {'a' : '9', 'b' : '15'},
            '13' : {'a' : '13', 'b' : '13'},
            '14' : {'a' : '14', 'b' : '14'},
            '15' : {'a' : '15', 'b' : '15'}
          },
        initial_state="0",
        final_states={"15"},
        )        

    with c2:
        # Add CFG within an expander
        my_expander = st.expander("Expand", expanded=True)
        with my_expander:
            st.write("S → ABCDEFBGB")
            st.write("A → bab | bbb")
            st.write("B → bB | aB | λ")
            st.write("C → abC | λ") 
            st.write("D → aba")
            st.write("E → babE | abaE | λ")
            st.write("F → bb")
            st.write("G → bab | aba")
  
if user_choice == r2:
    dfa = VisualDFA(
        states={'0', '1', '2','3','4', '5', '6','7','8', '9'},
        input_symbols={"0", "1"},
        transitions={ '0' : {'0' : '1', '1' : '2'},
            '1' : {'0' : '3', '1' : '0'},
            '2' : {'0' : '4', '1' : '4'},
            '3' : {'0' : '5', '1' : '6'},
            '4' : {'0' : '4', '1' : '6'},
            '5' : {'0' : '7', '1' : '8'},
            '6' : {'0' : '5', '1' : '6'},
            '7' : {'0' : '9', '1' : '8'},
            '8' : {'0' : '8', '1' : '8'},
            '9' : {'0' : '9', '1' : '9'}
          },
        initial_state="0",
        final_states={"8", "9"},
        )    

    with c2:
        y_expander = st.expander("Expand", expanded=True)
        with y_expander:
            st.write("S → ABCDAEAF")
            st.write("A → 0A | 1A | λ")
            st.write("B → 0B | λ")
            st.write("C → 1C | λ")
            st.write("D → 111 | 00 | 101")
            st.write("E → 101 | 01 | 000")
            st.write(" F → 101F | 001F |  λ")

# Load PDA images
if user_choice == r1:
    pda_image = Image.open("PDA1.png")
elif user_choice == r2:
    pda_image = Image.open("PDA 2.png")

# Limit the height of the image
aspect_ratio = pda_image.width / pda_image.height
new_height = min(pda_image.height, 500)
new_width = int(new_height * aspect_ratio)
pda_image_resized = pda_image.resize((new_width, new_height))

# Display PDA image
with c4:
    st.subheader("④ Pushdown Automaton (PDA)")
    st.image(pda_image_resized)

# String Checker and DFA Simulation code...

try:
    with c3:
        st.subheader("③  String Checker")
        string = st.text_input("Enter a String below to Simulate Automaton")
        test = st.button('Test')
           
    if test and not string:
        c3.write("You need to enter a string!")         
    elif user_choice == c1 or c2 and test:
        try: 
            checker = dfa.input_check(string)
            if "[Accepted]" in checker:
                result = "VALID ✅ "
                DFA = dfa.show_diagram(string)
            else:
                result = "INVALID ⭕ "
                DFA = dfa.show_diagram(string)
        except:
            result = "INVALID ⭕ "
        c3.write("**" + result + "**")
                  
    # ------------------------------------------------------------
    # Option B to Display DFA Simulation
    st.write(DFA)

    # ------------------------------------------------------------
    # Option A to Display DFA Simulation using base64
    
    # Reformat and save DFA as .svg
    DFA.format = "svg"
    DFA.render("automaton")

    # Open the saved .svg file from local directory
    s = open("automaton.svg", "r")
    lines = s.readlines()
    DFA_Final = ''.join(lines)

    # Display inputted string
    st.write("Transition graph for string **" + string + "**.")

    def render_svg(svg):
        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" alt="DFA" style="width:100%%; height:auto;">' % b64
        st.write(html, unsafe_allow_html=True)

    render_svg(DFA_Final)

except Exception as e:
    st.empty()
    print('Finished...')
    print(e)
