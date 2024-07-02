import streamlit as st
from .utils import (
    update_plugboard_connections,
    update_working_rotors,
    create_rotor_init_positon_slider,
)


def display_configuration__sidebar() -> None:
    """
    Display the configuration sidebar for the Enigma machine simulator.

    Allows users to select working rotors, set rotor initial positions,
    and configure plugboard connections.
    """
    # Configuration
    st.sidebar.header("Configuration :hammer_and_wrench:", divider="blue")

    # choose 3 working rotors out of 5 rotors
    st.sidebar.multiselect(
        "Select Working Rotors :gear:",
        options=["Rotor I", "Rotor II", "Rotor III", "Rotor IV", "Rotor V"],
        default=["Rotor I", "Rotor II", "Rotor III"],
        max_selections=3,
        key="working_rotor_names",
        on_change=lambda: update_working_rotors(),
    )

    # set rotors init position
    if st.session_state.show_slider:
        for i in range(3):
            create_rotor_init_positon_slider(i)

    # set plugboard connections
    st.sidebar.text_area(
        "Enter plugboard connections :electric_plug:",
        value=st.session_state.enigma_machine.config.pulgboard_connections,
        help=(
            "Enter pairs of letters separated by spaces. "
            "Each letter can only be used once. "
            "Only up to 10 connections are supported. "
            "(e.g., AB CD EF)"
        ),
        key="plugboard_input",
    )

    if st.sidebar.button("Apply Plugboard Connections"):
        update_plugboard_connections()

    st.sidebar.header("About")
    st.sidebar.info(
        """
        This app simulates the functionality of the Enigma machine,
        allowing you to encrypt and decrypt messages using configurable settings.
        """
    )
