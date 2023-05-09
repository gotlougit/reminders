# Reminders App

Just a simple reminders program to store and show reminders in an easy-to-use way. The entire data will be stored in an SQLite DB so it is easy to use programs like [Syncthing](https://syncthing.net/) in order to sync the reminders between different devices.

I built this mainly for myself since I didn't find a good program that could satisfy this requirement and I am not going to rely on cloud calendars or cloud services for this stuff. Besides, having reminders to do something is an easier workflow for me than using a calendar-based UI for some reason.

Right now it is a Python script for prototyping purposes, but later it will be an Android app (probably using React Native) and some Linux desktop variant (perhaps using Qt + CLI support, not sure about language choice yet).

## Current Roadmap

Right now, the plan is to get a basic Python script running. This will help when porting to Android since by this time we would have a working prototype running on desktop, and the Python script may even become the basis for the desktop client and/or the CLI.

Anyways, here are the goals:

- insert event either with date (so, important meeting coming up on 20/5/23) or with relative timing (ie, attend a meeting 4 hours from now)
- mark as recurring (frequency would have to be determined, is it annual, monthly, fortnightly, weekly, daily?)
- toggle recurring (remove recurring events or make other events recurring)
- remove event entirely
- notifications (likely just use a popular Python library for Linux notifications for the prototype)
