#!/usr/bin/python3

import time
import subprocess
import os
import sys
import cv2

# Check if Colorama has been already installed or not
try:
    from colorama import init, Fore
    print(Fore.LIGHTMAGENTA_EX + "Colorama has been already installed, We have initialized it for you :)")
    time.sleep(5)
except ImportError:
    print(Fore.RED + "Colorama has not been installed. Installing it...")
    subprocess.run(["pip", "install", "colorama"], check=True)
    from colorama import init, Fore
    print(Fore.LIGHTMAGENTA_EX + "Done, Colorama has been installed.")
    time.sleep(3)

# Clear the terminal screen
    os.system("clear")
    time.sleep(1)

def create_3d_banner():
    # Banner text
    banner_text = "CARTOONIZE"

    try:
        # Use figlet to create ASCII art with mono9 font
        figlet_process = subprocess.Popen(
            ["figlet", "-w", "27", "-f", "mono9", "-c", banner_text],
            stdout=subprocess.PIPE
        )
        figlet_output, _ = figlet_process.communicate()

        # Use lolcat to add color to the ASCII art
        lolcat_process = subprocess.Popen(["lolcat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        banner_output, _ = lolcat_process.communicate(input=figlet_output)

        # Print the result
        print(banner_output.decode())

    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + "Error: Make sure 'figlet' and 'lolcat' are installed on your system. (Hint: Run ./setup.sh)")
        time.sleep(2)

def cartoonize_video(input_path, output_path):
    try:
        # Open the input video file
        video_capture = cv2.VideoCapture(input_path)
        
        # Get the video codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        output_video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        while True:
            # Read the next frame from the video
            ret, frame = video_capture.read()
            
            # If frame is not read properly, break the loop
            if not ret:
                break
            
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply bilateral filter to reduce noise while preserving edges
            gray = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Apply median blur to smooth the image
            gray = cv2.medianBlur(gray, 7)
            
            # Detect edges using adaptive thresholding
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            
            # Convert edges image to color
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # Cartoonize the frame by combining edges with the original frame
            cartoonized_frame = cv2.bitwise_and(frame, edges)
            
            # Write the cartoonized frame to the output video
            output_video.write(cartoonized_frame)
        
        # Release video capture and writer objects
        video_capture.release()
        output_video.release()
        
        print(Fore.LIGHTMAGENTA_EX + "Cartoonization complete. Video saved to:\n", output_path + Fore.YELLOW)
        
    except Exception as e:
        print(Fore.LIGHTRED_EX + "An error occurred:", e + Fore.RED)

if __name__ == "__main__":
    try:
        # Get input and output file paths from the user
        input_path = input(Fore.CYAN + "Enter the filepath of the input video:\n \n")
        output_path = input(Fore.BLUE + "Enter the path to save the converted file:\n \n")
        
        # Ensure output path has .mp4 extension
        if not output_path.endswith(".mp4"):
            output_path += ".mp4"
        
        # Call the function to cartoonize the video
        cartoonize_video(input_path, output_path)
        
    except KeyboardInterrupt:
        print(Fore.LIGHTBLUE_EX + "\nConversion interrupted by user.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + "An error occurred:", e)


