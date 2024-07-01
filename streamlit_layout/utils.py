import streamlit as st
from src.enigma import EnigmaMachine


name_to_index = {
    "Rotor I": 0,
    "Rotor II": 1,
    "Rotor III": 2,
    "Rotor IV": 3,
    "Rotor V": 4,
}


def update_rotor_position(working_rotor_position: int) -> None:
    """
    Updates the position of a specified rotor in the Enigma 
    machine based on user selection.

    Args:
        working_rotor_position (int): Index of the rotor to update.
    """
    st.session_state.enigma_machine.set_rotors_position(
        working_rotor_position,
        st.session_state[f"rotor{working_rotor_position}_position"],
    )


def update_working_rotors() -> None:
    """
    Update the working rotors based on user selection.
    """
    match len(st.session_state["working_rotor_names"]):
        case 3:
            working_rotor_indices = [
                name_to_index[name] for name in st.session_state["working_rotor_names"]
            ]
            st.session_state.enigma_machine.choose_rotors(working_rotor_indices)
            st.session_state.rotor_miss = False
            st.session_state.show_slider = True
        case _:
            st.session_state.rotor_miss = True
            st.session_state.show_slider = False


def create_rotor_init_positon_slider(i: int) -> None:
    """
    Create a slider for setting the initial position of a rotor.

    Args:
        i (int): Index of the rotor for which the slider is created.
    """
    rotor = st.session_state.enigma_machine.working_rotors[i]
    st.sidebar.slider(
        f"Init Position of {rotor.name}:gear:",
        min_value=0,
        max_value=25,
        value=st.session_state.enigma_machine.config.rotors_init_position[i],
        step=1,
        key=f"rotor{i}_position",
        # Updates the Enigma machine's rotor
        # position when the slider value changes.
        on_change=lambda: update_rotor_position(i),
    )


def update_plugboard_connections() -> None:
    """
    Update the plugboard connections based on user input.
    """
    try:
        st.session_state.enigma_machine.set_plugboard(st.session_state.plugboard_input)
        st.session_state.plugboard_invalid = False
        for i in range(3):
            update_rotor_position(i)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.warning("Please check your plugboard connections and try again.")
        st.session_state.plugboard_invalid = True


def display_rotor_position(rotor_name: str, position: int, notch: int) -> None:
    """
    Displays the current position of a rotor, with indicators for the rotor's
    current position and notch.

    Args:
        rotor_name (str): Name of the rotor.
        position (int): Current position of the rotor.
        notch (int): Notch position of the rotor.
    """
    st.write(f"{rotor_name}: ")
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    chars[position] = f"[{chars[position]}]"
    chars[notch] = f"*{chars[notch]}*"
    st.code("".join(chars))


def display_enigma_config(machine: EnigmaMachine):
    """
    Retrieves and displays the current positions and notch settings
    of the working rotors, as well as the plugboard connections.

    Args:
        machine (EnigmaMachine): Instance of the Enigma machine 
            to display the configuration for.
    """
    rotors = machine.working_rotors
    notchs = [rotor.notch for rotor in rotors]
    positions = machine.get_working_rotors_position()
    for i in range(3):
        display_rotor_position(rotors[i].name, positions[i], notchs[i])
    st.write("Plugboard Connections:")
    st.code(machine.plugboard.get_plugboard_connections())
