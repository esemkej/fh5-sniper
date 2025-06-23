First of all, if you want to edit and publish this program in any way, feel free to do so, but please credit me.

How this program works:  
It's a simple script that automatically presses the correct keys to refresh and buy auctions. To see if there's an active auction it checks the correct pixel for correct white color with some headroom. After it tries to buy out the auction, it waits a little and checks another pixel to see if the buyout was successful or not, to avoid any unwanted behaviour. Even though the script itself is around 12KB, the file size is 45MB because I'm using pyinstaller --onefile which packs a whole lot of stuff inside the exe.

**The code takes a while to initalize itself, so if you're looking at a clear cmd, everything is working as it's supposed to, just give it a few seconds**  
Use tutorial:  
**1. If you're running an aspect ratio different from 16:9, you have to toggle full-screen off, otherwise you'll find yourself with an infinite sniper**  
2. Lock your fps at a stable value to avoid any issues  
3. Go in to the auctions tab and search for the vehicle you'd like to snipe  
4. You can toggle infinite sniping by pressing **I**  
5. **Make sure the focused window in the auction house is the search for auctions one** and then press **S** and just let it run  
6. If you toggled infinite sniping, the script will continue to snipe cars after buying the first one, otherwise it would go back to the auction house and stop  
  
If there are any issues, reread this readme first and if nothing works, feel free to leave an issue message, I'll try to look at it asap.

**What to expect with new releases:**  
1. From the user's standpoint? Probably nothing for now
2. From the dev's standpoint? Code wrapped in classes so it's more readable
