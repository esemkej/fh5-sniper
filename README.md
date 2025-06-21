First of all, if you want to edit and publish this file in any way, feel free to do so, but please credit me.

How this program works:
It's a simple script that automatically presses the correct keys to refresh and buy auctions. The pixel thing is there because to know if an auction is active, it has to check the color of that specific pixel. If the color's white, it launches the buy process.
To make sure it works correctly, always line up your cursor in the middle of any active auction where there's no text whatsoever and only then press P. Even though the script itself is around 12KB, the file size is 45MB because I'm using pyinstaller --onefile which packs a whole lot of stuff inside the exe.

Use tutorial:
1. Lock your fps at a stable value to avoid any issues, you don't have to turn off fulscreen
2. Go in to the auctions tab and search for any vehicle that is always selling
3. Open the app and press the "Pick coordinates" button
4. Go back to actuions and line up your mouse cursor with the middle of the 1st auction, and make sure it's somewhere where the listing is always white and press P. No text no nothing, otherwise it won't work correctly.
5. After that, you should see see "Checking: x, y" (the program autosaves these coordinates inside the json, but if it shows an error message, you don't really have to worry, it just can't access the json file, but it should still work)
6. Now search for the car that you want to snipe and after that go back to the auctions tab
7. If you want, you can toggle infinite sniping (program continues to snipe the car even if it already bought it successfully)
8. Now just press S and let it run, it will collect the car automatically

If there are any issues, try to pick coordinates again, reread this readme and if nothing works, feel free to leave issue message, I'll try to look at it asap
