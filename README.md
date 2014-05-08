AeroChat
===

AeroChat is a secure chat service built on top of the AeroFS cloud platform.

Your messages are transferred via AeroFS channels and are only accessible by you and the intended recipients of your message. No third party can view your messages. Ever.

This project is a work in progress and was originally developed during a hackathon at AeroFS HQ.

Usage
---

To run AeroChat, download the aerochat executable and place it in an AeroFS shared folder. Double click on the application and an AeroChat chatroom will open. All members of the shared folder can participate in this chatroom.

Supported platforms: Mac OS X and common Linux distributions. Tested on Ubuntu 12.04 LTS.

Developers
---
Use the following command to run the unit tests for this project:

    python src/run_tests.py

To build a new AeroChat executable, simply run `./build.sh`. I will periodically commit updated `aerochat` executables, so the version in this repository should satisfy the needs of most.
