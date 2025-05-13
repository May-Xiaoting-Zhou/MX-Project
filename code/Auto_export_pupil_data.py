import os
import time
import subprocess
import pyautogui

EXAM_FOLDER_PATH = "/Users/xiaotingzhou/Downloads/Pupil_Exam"
PUPIL_PLAYER_PATH = "/Applications/Pupil Player.app"
DELAY_LAUNCH = 7  # Increased launch time
DELAY_EXPORT = 10  # Longer export timeout

def process_folder(folder_path):
    try:
        # Proper AppleScript for drag-and-drop simulation
        script = f'''
        tell application "{PUPIL_PLAYER_PATH}"
            activate
            delay 2
            open POSIX file "{folder_path}"
        end tell
        '''
        
        # Execute AppleScript with proper escaping
        subprocess.run([
            'osascript',
            '-e', script
        ], check=True)
        
        time.sleep(DELAY_LAUNCH)
        
        # Send export command
        pyautogui.press('e')
        time.sleep(DELAY_EXPORT)
        
        # Ensure clean quit
        subprocess.run([
            'osascript',
            '-e', 'tell application "Pupil Player" to quit'
        ])
        
    except Exception as e:
        print(f"Error processing {folder_path}: {str(e)}")

def main():
    # Get list of folders sorted numerically
    folders = sorted(
        [f for f in os.listdir(EXAM_FOLDER_PATH) 
         if os.path.isdir(os.path.join(EXAM_FOLDER_PATH, f))],
        key=lambda x: int(x.split('_')[1])  # Assuming Sub_XX format
    )

    for folder in folders:
        folder_path = os.path.join(EXAM_FOLDER_PATH, folder)
        print(f"Processing: {folder_path}")
        process_folder(folder_path)
    
    print("All exports completed.")

if __name__ == "__main__":
    main()