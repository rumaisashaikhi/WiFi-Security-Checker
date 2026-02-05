import subprocess

def scan_wifi():
    print("Scanning nearby WiFi networks...\n")

    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True
    )

    output = result.stdout.split("\n")

    networks = []
    current_network = {}

    for line in output:
        line = line.strip()

        if line.startswith("SSID"):
            if current_network:
                networks.append(current_network)
                current_network = {}
            current_network["SSID"] = line.split(":")[1].strip()

        elif "Authentication" in line:
            current_network["Security"] = line.split(":")[1].strip()

        elif "Signal" in line:
            current_network["Signal"] = line.split(":")[1].strip()

    if current_network:
        networks.append(current_network)

    print("\nWiFi Security Report:\n")

    for net in networks:
        ssid = net.get("SSID", "Unknown")
        sec = net.get("Security", "Unknown")
        signal = net.get("Signal", "Unknown")

        print(f"Network: {ssid}")
        print(f"Security: {sec}")
        print(f"Signal Strength: {signal}")

        if "Open" in sec:
            print("⚠ WARNING: This network has NO encryption!")
        elif "WEP" in sec:
            print("⚠ Weak security (WEP is outdated)")
        elif "WPA2" in sec:
            print("✔ Reasonably secure")
        elif "WPA3" in sec:
            print("🔐 Strong modern security")

        print("-" * 40)


scan_wifi()
