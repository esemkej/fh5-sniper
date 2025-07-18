First of all, if you want to edit and publish this program in any way, feel free to do so, but please credit me.

How this program works:  
It's a simple script that automatically presses the correct keys to refresh and buy auctions. To see if there's an active auction it checks the correct pixel for correct white color with some headroom. After it tries to buy out the auction, it waits a little and checks another pixel to see if the buyout was successful or not, to avoid any unwanted behaviour. It supports 3 different methods of sniping which are described below. Even though the script itself is around 16KB, the file size is 45MB because I'm using pyinstaller --onefile which packs a whole lot of stuff inside the exe.  
**Sniping methods:**  
**1. Safe sniping:** This will always pick a slightly random value of how much time it should wait between inputs, making it less detectable if there's any detection present. This will also work on lower fps and **I advise you to keep using this one** unless it's necessary for you to use a different one.  
**2. Normal sniping:** This is the basic method from older versions but it's deprecated. Will also work nicely on lower fps.  
**3. Quick sniping:** This is a highly experimental method where I tried to minimize the wait time between inputs. It starts to break down under 120fps but try to get more (e.g. 144fps, 165fps...) to avoid issues. I don't advise you to use it unless absolutely necessary, for example when encountering car that is in such a high demand, the normal sniping doesn't stand a chance.

**The code takes a while to initalize itself, so if you're looking at a clear cmd, everything is working as it's supposed to, just give it a few seconds**  
Use tutorial:  
**1. If you're running an aspect ratio different from 16:9, you have to toggle full-screen off, otherwise you'll find yourself with an infinite sniper**  
2. Lock your fps at a stable value to avoid any issues  
3. Go in to the auctions tab and search for the vehicle you'd like to snipe  
4. You can toggle infinite sniping by pressing the designated button  
5. **Make sure the focused window in the auction house is the search for auctions one** and then press **S** and just let it run  
6. If you toggled infinite sniping, the script will continue to snipe cars after buying the first one, otherwise it would go back to the auction house and stop  

**Custom sniping**  
This tool also has an option for custom sniping where you can directly change all the timings as well as pixel position to really fine tune it for your pc. I suppose that with this option, you should be able to use this bot with any screen res as well as ratio.  
The app also displays default values (taken from normal sniping) in case you want to keep some timings as they were (highly recommended)

If there are any issues, reread this readme first and if nothing works, feel free to leave an issue message, I'll try to look at it asap.

**What to expect with new releases:**  
Fully cmd operated version without any UI whatsoever in case the UI version causes bugs.
