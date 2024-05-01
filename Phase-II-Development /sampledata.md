            Timestamp              Source IP       Destination IP    Protocol   Port   Alert Type       Severity
            -----------------------------------------------------------------------------------------------
            2024-05-01 08:15:23    192.168.1.10    203.0.113.1       TCP        22     SSH Brute Force  High
            2024-05-01 08:17:45    10.0.0.5        198.51.100.2      UDP        53     DNS Query        Medium
            2024-05-01 08:20:10    192.168.1.20    198.51.100.3      TCP        445    SMB Recon        Low
            2024-05-01 08:22:30    192.168.1.30    203.0.113.2       ICMP       -      Ping Sweep       High

    Timestamp: Date and time when the security event was detected.
    Source IP: IP address of the network device initiating the connection.
    Destination IP: IP address of the target device or server.
    Protocol: Network protocol used for the communication (e.g., TCP, UDP, ICMP).
    Port: Destination port number.
    Alert Type: Type of security alert triggered by the IDS (e.g., SSH Brute Force, DNS Query, SMB Recon, Ping Sweep).
    Severity: Severity level of the security alert (e.g., Low, Medium, High).

In this example, the IDS is monitoring network traffic and generating alerts for suspicious or malicious activity detected on the network. Each row represents a security event captured by the IDS, including details such as the source and destination IP addresses, the protocol and port used for communication, the type of alert triggered, and the severity level of the alert.

This real-time cybersecurity data can be continuously streamed to a data analytics pipeline for further analysis, correlation, and response. By analyzing this data in real-time, security teams can identify and respond to security threats promptly, helping to protect the organization's network infrastructure and sensitive data from cyberattacks.
