import streamlit as st
from .utils import display_enigma_config


def display_main_view() -> None:
    """
    Display the main view of the Enigma machine simulator.

    Allows users to enter text for encryption or decryption,
    process the input, and display the result along with the current
    state of the Enigma machine.
    """
    # Main App
    text_input = st.text_area("Enter text to encrypt or decrypt:", height=150)

    if st.session_state.plugboard_invalid:
        st.warning(
            "Plugboard configuration is invalid. Please correct it before processing."
        )
        st.button("Process", disabled=True)
    else:
        if st.button("Process"):
            try:
                if st.session_state["rotor_miss"]:
                    st.error("Please select 3 rotors to run the machine.")
                else:
                    result = st.session_state.enigma_machine(text_input)
                    st.success(f"Result:\n{result}")
                    # Current state
                    with st.expander("Current Enigma State"):
                        display_enigma_config(st.session_state.enigma_machine)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.warning("Please check your input and try again.")
