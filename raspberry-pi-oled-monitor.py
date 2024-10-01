import time
import subprocess
from collections import deque
import os

# Import necessary modules for I2C communication and display handling
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create the I2C interface using the board's SCL and SDA pins
i2c = busio.I2C(SCL, SDA)

# Initialize the SSD1306 OLED display connected via I2C
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear the display buffer
disp.fill(0)
disp.show()

# Get display width and height for creating images
width = disp.width
height = disp.height

# Create a blank image with mode '1' for 1-bit color
image = Image.new("1", (width, height))

# Create a drawing object to draw on the image
draw = ImageDraw.Draw(image)

# Define fonts of various sizes
font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)  # Large font for scrolling text
font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)    # Small font for labels
font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)     # Tiny font for detailed info

# Define the text to scroll across the top of the display
scroll_text = "Your hostname here"

# Calculate the width of the scrolling text for proper wrapping
bbox = font_large.getbbox(scroll_text)
maxwidth = bbox[2] - bbox[0]

# Initialize scrolling variables
offset = width               # Starting offset (from the right edge)
scroll_speed = 8             # Speed of scrolling text
last_scroll_time = time.time()
scroll_interval = 0.01       # Interval between scroll updates

# Define the list of stats to display and initialize index and timing
stats = ['CPU Load', 'Memory Usage', 'Disk Usage', 'Docker Containers', 'System Info']
stat_index = 0
last_switch_time = time.time()

# Initialize data deques to store historical data for graphs
max_data_points = width      # Number of data points equals display width
cpu_data = deque([0]*max_data_points, maxlen=max_data_points)
mem_data = deque([0]*max_data_points, maxlen=max_data_points)
disk_data = deque([0]*max_data_points, maxlen=max_data_points)

while True:
    # Get the current time for timing calculations
    current_time = time.time()

    # Update scrolling text offset if enough time has passed
    if current_time - last_scroll_time >= scroll_interval:
        offset -= scroll_speed          # Move text to the left
        last_scroll_time = current_time
        if offset < -maxwidth:
            offset = width              # Reset offset when text has scrolled off

    # Clear the image by drawing a black rectangle
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw the scrolling text at the top
    x_offset = offset
    draw.text((x_offset, 0), scroll_text, font=font_large, fill=255)

    # Calculate positions for the stats and graphs
    scroll_text_y = 0
    bbox = font_large.getbbox(scroll_text)
    scroll_text_height = bbox[3] - bbox[1]
    value_text_y = scroll_text_y + scroll_text_height + 1    # Adjusted to move stats down by 1 pixel
    bbox_small = font_small.getbbox("A")
    value_text_height = (bbox_small[3] - bbox_small[1]) + 2  # Height of small font plus spacing
    graph_y = value_text_y + value_text_height + 1           # Adjusted to move graph down by 1 pixel
    graph_height = height - graph_y

    # Switch to the next stat every 3 seconds
    if current_time - last_switch_time > 3:
        stat_index = (stat_index + 1) % len(stats)
        last_switch_time = current_time

    # Display the appropriate screen based on the current stat index
    if stats[stat_index] == 'CPU Load':
        # Get CPU load using shell command
        cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
        CPU = float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip())
        cpu_data.append(CPU)                   # Add current CPU load to deque
        graph_data = list(cpu_data)
        label = "CPU Load"
        value = f"{CPU:.1f}%"

        # Draw the label and value
        draw.text((0, value_text_y), f"{label}: {value}", font=font_small, fill=255)

        # Prepare data for graph scaling
        scaled_data = [graph_height - int((v / 100.0) * graph_height) for v in graph_data]

        # Draw the line graph for CPU load
        for x in range(len(scaled_data) - 1):
            draw.line([(x, graph_y + scaled_data[x]), (x + 1, graph_y + scaled_data[x + 1])], fill=255)
            draw.line([(x, graph_y + scaled_data[x]), (x, graph_y + graph_height)], fill=255)

    elif stats[stat_index] == 'Memory Usage':
        # Get memory usage using shell command
        cmd = "free -m | awk 'NR==2{printf \"%s %s\", $3,$3*100/$2 }'"
        mem_used_str, mem_percent_str = subprocess.check_output(cmd, shell=True).decode("utf-8").split()
        mem_used = float(mem_used_str)
        mem_percent = float(mem_percent_str)
        mem_data.append(mem_percent)           # Add current memory usage to deque
        graph_data = list(mem_data)
        label = "Memory"
        value = f"{mem_used:.0f}MB ({mem_percent:.1f}%)"

        # Draw the label and value
        draw.text((0, value_text_y), f"{label}: {value}", font=font_small, fill=255)

        # Prepare data for graph scaling
        scaled_data = [graph_height - int((v / 100.0) * graph_height) for v in graph_data]

        # Draw the line graph for memory usage
        for x in range(len(scaled_data) - 1):
            draw.line([(x, graph_y + scaled_data[x]), (x + 1, graph_y + scaled_data[x + 1])], fill=255)
            draw.line([(x, graph_y + scaled_data[x]), (x, graph_y + graph_height)], fill=255)

    elif stats[stat_index] == 'Disk Usage':
        # Get disk usage using shell command
        cmd = 'df -BG / | awk \'NR==2{printf "%d %s", $3,$5}\' | tr -d "%"'
        disk_used_str, disk_percent_str = subprocess.check_output(cmd, shell=True).decode("utf-8").split()
        disk_used = int(disk_used_str)
        disk_percent = float(disk_percent_str)
        disk_data.append(disk_percent)         # Add current disk usage to deque
        graph_data = list(disk_data)
        label = "Disk"
        value = f"{disk_used}GB ({disk_percent:.1f}%)"

        # Draw the label and value
        draw.text((0, value_text_y), f"{label}: {value}", font=font_small, fill=255)

        # Prepare data for graph scaling
        scaled_data = [graph_height - int((v / 100.0) * graph_height) for v in graph_data]

        # Draw the line graph for disk usage
        for x in range(len(scaled_data) - 1):
            draw.line([(x, graph_y + scaled_data[x]), (x + 1, graph_y + scaled_data[x + 1])], fill=255)
            draw.line([(x, graph_y + scaled_data[x]), (x, graph_y + graph_height)], fill=255)

    elif stats[stat_index] == 'Docker Containers':
        # Get Docker container information
        cmd = "docker ps --format '{{.Names}}|{{.CreatedAt}}|{{.Status}}'"
        try:
            docker_output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            containers = docker_output.split('\n')
        except subprocess.CalledProcessError:
            containers = []

        label = "Docker Containers"
        draw.text((0, value_text_y), label, font=font_small, fill=255)

        container_y = graph_y

        # Calculate line height for container details
        bbox_tiny = font_tiny.getbbox("A")
        line_height = (bbox_tiny[3] - bbox_tiny[1]) + 2

        # Calculate maximum number of containers that can be displayed
        max_containers = (height - container_y) // line_height

        # Display container names and statuses
        for idx, container in enumerate(containers[:max_containers]):
            try:
                name, created_at, status = container.split('|')
                display_text = f"{name}: {status}"
                draw.text((0, container_y + idx * line_height), display_text, font=font_tiny, fill=255)
            except ValueError:
                continue  # Skip if parsing fails

    elif stats[stat_index] == 'System Info':
        # Get OS version
        try:
            cmd = 'lsb_release -ds'
            os_version = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().strip('"')
        except subprocess.CalledProcessError:
            os_version = 'Unknown OS'

        # Get last patched date
        try:
            apt_history = '/var/log/apt/history.log'
            last_patched_timestamp = os.path.getmtime(apt_history)
            last_patched = time.strftime('%Y-%m-%d %H:%M', time.localtime(last_patched_timestamp))
        except Exception:
            last_patched = 'Unknown'

        # Check if reboot is pending
        reboot_required = os.path.isfile('/var/run/reboot-required')
        reboot_status = 'Yes' if reboot_required else 'No'

        label = 'System Info'
        draw.text((0, value_text_y), label, font=font_small, fill=255)

        info_y = graph_y

        # Define the lines of system info to display
        info_lines = [
            f"OS: {os_version}",
            f"Last Patched:",
            f"{last_patched}",
            f"Reboot Pending: {reboot_status}"
        ]

        # Set font for system info
        info_font = font_small

        # Calculate line height
        bbox_info = info_font.getbbox("A")
        line_height = (bbox_info[3] - bbox_info[1]) + 2

        # Display each line of system info
        for idx, line in enumerate(info_lines):
            y_position = info_y + idx * line_height
            if y_position + line_height > height:
                break  # Stop if we run out of space
            draw.text((0, y_position), line, font=info_font, fill=255)

    else:
        pass  # Should not reach here

    # Update the display with the new image
    disp.image(image)
    disp.show()
    time.sleep(0.20)  # Delay to control update frequency
