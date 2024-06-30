import streamlit as st
from src.enigma import EnigmaMachine, EnigmaMachineConfig


name_to_index = {
    "Rotor I": 0,
    "Rotor II": 1,
    "Rotor III": 2,
    "Rotor IV": 3,
    "Rotor V": 4,
}


def update_rotor_position(working_rotor_position):
    st.session_state.enigma_machine.set_rotors_position(
        working_rotor_position,
        st.session_state[f"rotor{working_rotor_position}_position"],
    )


def update_working_rotors():
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

def create_rotor_init_positon_slider(i):
    rotor = st.session_state.enigma_machine.working_rotors[i]
    st.sidebar.slider(
        f"Init Position of {rotor.name}",
        min_value=0,
        max_value=25,
        value=st.session_state.enigma_machine.config.rotors_init_position[i],
        step=1,
        key=f"rotor{i}_position",
        on_change=lambda: update_rotor_position(i),
    )

def update_plugboard_connections():
    try:
        st.session_state.enigma_machine.set_plugboard(
            st.session_state.plugboard_input
        )
        st.session_state.plugboard_invalid = False
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.warning("Please check your plugboard connections and try again.")
        st.session_state.plugboard_invalid = True


def display_rotor_position(rotor_name, position, notch):
    st.write(f"{rotor_name}: ")
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    chars[position] = f"[{chars[position]}]"
    chars[notch] = f"*{chars[notch]}*"
    st.code("".join(chars))


def display_enigma_config(machine: EnigmaMachine):
    rotors = machine.working_rotors
    notchs = [rotor.notch for rotor in rotors]
    positions = machine.get_working_rotors_position()
    for i in range(3):
        display_rotor_position(rotors[i].name, positions[i], notchs[i])
    st.write("Plugboard Connections: ")
    st.code(machine.plugboard.get_plugboard_connections())


def main():
    st.title("Enigma Machine Simulator")
    enigma_config = EnigmaMachineConfig()
    # Initialize enigma_machine in session state
    if "enigma_machine" not in st.session_state:
        st.session_state.enigma_machine = EnigmaMachine(enigma_config)
        st.session_state.rotor_miss = False
        st.session_state.show_slider = True
        st.session_state.plugboard_invalid = False

    # Configuration
    st.sidebar.header("Configuration")

    # choose 3 working rotors out of 5 rotors
    st.sidebar.multiselect(
        "Select Working Rotors",
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
        "Enter plugboard connections (e.g., AB CD EF):",
        value=st.session_state.enigma_machine.config.pulgboard_connections,
        help=(
            "Enter pairs of letters separated by spaces. "
            "Each letter can only be used once. "
            "Only up to 10 connections are supported."
        ),
        key="plugboard_input",
    )
    if st.sidebar.button("Apply Plugboard Connections"):
        update_plugboard_connections()

    # Main App
    st.subheader("Enigma Machine Simulation")
    text_input = st.text_area("Enter text to encrypt or decrypt:", height=150)

    if st.session_state.plugboard_invalid:
        st.warning("Plugboard configuration is invalid. Please correct it before processing.")
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

    st.sidebar.header("About")
    st.sidebar.info(
        """
        This app simulates the functionality of the Enigma machine,
        allowing you to encrypt and decrypt messages using configurable settings.
        """
    )


if __name__ == "__main__":
    main()
