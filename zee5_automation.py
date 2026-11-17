#!/usr/bin/env python3
"""
ZEE5 & Device Automation Script via ADB
---------------------------------------
Automates:
1. Device connection verification (Realme RMX3430 / Android device).
2. Screen wake up & keyguard dismissal.
3. YouTube launch & termination.
4. ZEE5 launch and promotional ad dismissal.
5. ZEE5 Login using Mobile Number + OTP.
6. Search and selection of content ("Sumo Didi").
"""

import subprocess
import time
import sys
import xml.etree.ElementTree as ET

# Package Identifiers
YOUTUBE_PKG = "com.google.android.youtube"
ZEE5_PKG = "com.graymatrix.did"
ADB_BIN = "/opt/homebrew/bin/adb"


def run_adb(cmd: str) -> str:
    """Executes an ADB command and returns standard output."""
    full_cmd = f"{ADB_BIN} {cmd}"
    try:
        res = subprocess.run(
            full_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ADB Error] {cmd}: {e.stderr.strip()}", file=sys.stderr)
        return ""


def check_device():
    """Checks ADB device connectivity and authorization."""
    print("[1/6] Checking connected ADB devices...")
    output = run_adb("devices -l")
    print(output)
    if "device usb:" not in output and "device " not in output:
        raise RuntimeError("No authorized ADB device found. Please enable USB Debugging.")
    
    brand = run_adb("shell getprop ro.product.brand")
    model = run_adb("shell getprop ro.product.model")
    android_ver = run_adb("shell getprop ro.build.version.release")
    print(f"Connected to: {brand.upper()} {model} (Android {android_ver})\n")


def wake_device():
    """Wakes the screen and dismisses standard keyguard."""
    print("[*] Waking screen...")
    run_adb("shell input keyevent KEYCODE_WAKEUP")
    run_adb("shell wm dismiss-keyguard")
    time.sleep(1)


def launch_youtube():
    """Launches YouTube."""
    print("[2/6] Launching YouTube...")
    wake_device()
    run_adb(f"shell monkey -p {YOUTUBE_PKG} -c android.intent.category.LAUNCHER 1")
    time.sleep(3)
    print("YouTube launched successfully.\n")


def kill_and_launch_zee5():
    """Kills YouTube and opens ZEE5 cleanly."""
    print("[3/6] Killing YouTube & launching ZEE5...")
    run_adb(f"shell am force-stop {YOUTUBE_PKG}")
    run_adb(f"shell am force-stop {ZEE5_PKG}")
    time.sleep(1)
    
    wake_device()
    run_adb(f"shell monkey -p {ZEE5_PKG} -c android.intent.category.LAUNCHER 1")
    print("Waiting for ZEE5 to initialize...")
    time.sleep(4)


def dismiss_popup_ad():
    """Closes the promotional ad banner on app start."""
    print("[4/6] Dismissing promotional ad popup...")
    # Taps the 'X' close button at top right of the in-app ad modal (bounds: [644,133][720,213])
    run_adb("shell input tap 682 173")
    time.sleep(2)
    print("Ad dismissed.\n")


def login_zee5(mobile_number: str = "9008882827"):
    """Navigates to Profile, enters mobile number, and prompts for OTP."""
    print(f"[5/6] Logging in with mobile number: {mobile_number}...")
    
    # 1. Tap Profile tab in bottom navigation (bounds: [521,1366][682,1448])
    run_adb("shell input tap 601 1407")
    time.sleep(2)
    
    # 2. Tap 'Log In / Sign Up' box
    run_adb("shell input tap 360 438")
    time.sleep(2)
    
    # 3. Enter mobile number
    run_adb(f"shell input text {mobile_number}")
    time.sleep(1)
    
    # 4. Tap 'Verify To Continue' button (bounds: [32,652][688,764])
    run_adb("shell input tap 360 708")
    time.sleep(2)
    
    # 5. Prompt user for OTP
    otp = input("Enter the 4-digit OTP received on your phone: ").strip()
    if otp:
        print(f"Submitting OTP: {otp}...")
        run_adb(f"shell input text {otp}")
        time.sleep(1)
        # Tap Verify button
        run_adb("shell input tap 360 724")
        time.sleep(3)
        print("Login completed!\n")


def search_and_select_content(query: str = "Sumo Didi"):
    """Navigates to Search, searches for query, and selects it."""
    print(f"[6/6] Searching and selecting '{query}'...")
    
    # 1. Tap Search tab (bounds: [360,1366][521,1448])
    run_adb("shell input tap 440 1407")
    time.sleep(2)
    
    # 2. Tap search input field (bounds: [106,96][688,208])
    run_adb("shell input tap 350 152")
    time.sleep(1)
    
    # 3. Enter search query (replacing spaces with %s for ADB)
    formatted_query = query.replace(" ", "%s")
    run_adb(f"shell input text {formatted_query}")
    time.sleep(1)
    
    # 4. Press Enter / Search key
    run_adb("shell input keyevent 66")
    time.sleep(2)
    
    # 5. Select the content (tap on 'Watch' or poster bounds: [234,660][442,756])
    print(f"Selecting '{query}'...")
    run_adb("shell input tap 338 708")
    time.sleep(2)
    print(f"'{query}' selected successfully!")


def main():
    check_device()
    wake_device()
    
    # Step-by-step execution flow:
    # 1. Launch YouTube
    # launch_youtube()
    
    # 2. Kill and Launch ZEE5
    kill_and_launch_zee5()
    
    # 3. Dismiss initial ad
    dismiss_popup_ad()
    
    # 4. Login flow
    # login_zee5("9008882827")
    
    # 5. Search & select content
    search_and_select_content("Sumo Didi")
    
    print("\n[Done] All automated steps executed successfully.")


if __name__ == "__main__":
    main()
