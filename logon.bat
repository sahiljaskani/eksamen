@echo off

:: Map network drives
net use X: \\fileserver\sharedfolder

:: Set environment variables
set PATH=%PATH%;C:\Program Files\MyApp

:: Run a program
start C:\Program Files\MyApp\myapp.exe

:: Display a message
echo Welcome to Gamasjer A/S!

:: Play a sound
start C:\Windows\Media\chimes.wav
