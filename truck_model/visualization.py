import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(filename='model_logs.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def plot_data(t, rms_vibration, speed, voltage, labels):
        # Plot the data
        plt.figure(figsize=(14, 10))

        # Define state colors
        state_colors = {'ACTIVE': 'green', 'IDLE': 'yellow', 'OFF': 'red'}

        # Function to add state color index
        def add_state_color_index(ax, state_colors):
            handles = [plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.3) for color in state_colors.values()]
            labels = state_colors.keys()
            ax.legend(handles, labels, title="State", loc='upper right')

        # Plot RMS Vibration
        plt.subplot(3, 1, 1)
        plt.plot(t, rms_vibration, label='RMS Vibration')
        current_time = 0
        for i in range(len(labels)):
            if i == 0 or labels[i] != labels[i - 1]:
                state = labels[i]
                start = t[i]
                if i > 0:
                    plt.axvline(x=start, color='black', linestyle='--', alpha=0.5)
            if i == len(labels) - 1 or labels[i] != labels[i + 1]:
                end = t[i]
                if state == 'ACTIVE':
                    plt.axvspan(start, end, color=state_colors['ACTIVE'], alpha=0.3, label='ACTIVE' if start == t[0] else "")
                elif state == 'IDLE':
                    plt.axvspan(start, end, color=state_colors['IDLE'], alpha=0.3, label='IDLE' if start == t[0] else "")
                elif state == 'OFF':
                    plt.axvspan(start, end, color=state_colors['OFF'], alpha=0.3, label='OFF' if start == t[0] else "")
        plt.xlabel('Time (s)')
        plt.ylabel('RMS Vibration')
        plt.title('RMS Vibration Over Time')
        add_state_color_index(plt.gca(), state_colors)  # Add state color index

        # Plot Speed
        plt.subplot(3, 1, 2)
        plt.plot(t, speed, label='Speed')
        current_time = 0
        for i in range(len(labels)):
            if i == 0 or labels[i] != labels[i - 1]:
                state = labels[i]
                start = t[i]
                if i > 0:
                    plt.axvline(x=start, color='black', linestyle='--', alpha=0.5)
            if i == len(labels) - 1 or labels[i] != labels[i + 1]:
                end = t[i]
                if state == 'ACTIVE':
                    plt.axvspan(start, end, color=state_colors['ACTIVE'], alpha=0.3)
                elif state == 'IDLE':
                    plt.axvspan(start, end, color=state_colors['IDLE'], alpha=0.3)
                elif state == 'OFF':
                    plt.axvspan(start, end, color=state_colors['OFF'], alpha=0.3)
        plt.xlabel('Time (s)')
        plt.ylabel('Speed (km/h)')
        plt.title('Speed Over Time')
        add_state_color_index(plt.gca(), state_colors)  # Add state color index

        # Plot Voltage
        plt.subplot(3, 1, 3)
        plt.plot(t, voltage, label='Voltage')
        current_time = 0
        for i in range(len(labels)):
            if i == 0 or labels[i] != labels[i - 1]:
                state = labels[i]
                start = t[i]
                if i > 0:
                    plt.axvline(x=start, color='black', linestyle='--', alpha=0.5)
            if i == len(labels) - 1 or labels[i] != labels[i + 1]:
                end = t[i]
                if state == 'ACTIVE':
                    plt.axvspan(start, end, color=state_colors['ACTIVE'], alpha=0.3)
                elif state == 'IDLE':
                    plt.axvspan(start, end, color=state_colors['IDLE'], alpha=0.3)
                elif state == 'OFF':
                    plt.axvspan(start, end, color=state_colors['OFF'], alpha=0.3)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (mV)')
        plt.title('Voltage Over Time')
        add_state_color_index(plt.gca(), state_colors)  # Add state color index

        plt.tight_layout()
        plt.savefig('output_plot.png', bbox_inches='tight')