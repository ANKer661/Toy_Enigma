import streamlit as st

from src.enigma import EnigmaMachine, EnigmaMachineConfig
from streamlit_layout.main_view import display_main_view
from streamlit_layout.side_bar import display_configuration__sidebar


def initialize_session_state():
    # Initialize enigma_machine in session state
    if "enigma_machine" not in st.session_state:
        enigma_config = EnigmaMachineConfig()
        st.session_state.enigma_machine = EnigmaMachine(enigma_config)
        st.session_state.rotor_miss = False
        st.session_state.show_slider = True
        st.session_state.plugboard_invalid = False


def main():
    st.title("Enigma Machine Simulator")

    initialize_session_state()

    display_configuration__sidebar()

    display_main_view()


if __name__ == "__main__":
    main()
