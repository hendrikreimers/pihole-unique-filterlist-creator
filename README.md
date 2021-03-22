# PI-HOLE Unique Big Blacklist
Helps to create a really big filter blacklist for pi-hole with unique domains


## What does is do or not?
It's a really small not perfect script, but works well :-)

The python script gets all files from the URLs listed in the ***urlLists/_nearly-all.txt***
and builds a unique blocking list in ***/dist/_nearly-all.txt***

The multi script does the same but takes or text files starting with "list-..." and builds categorized lists.

By the way, it fixes some of the lists which are not having the correct IP for the blacklist and removes comments.

## The Lists

See in the **dist** folder for the list results
See in the **urlLists** folder for the URLs

### Blacklist
Run the python script (build.py), maybe on your webserver or someone else
and import the URL to your pihole blacklist adlist as only one single list.

Or you could check it out on your pihole and add it as cronjob to build it in /var/www/html/pihole/blacklist.txt or somewhere else

#### Multiple Blacklists

Run the **build-multi.py** (or binary) for build categorizes lists. See dists/ folder for results

**But beware**

If you build multiple lists, it's possible that some domains are not unique over all. 
Thats rises the file size, too.

### Whitelist
You must include the whitelist by the admin panel or the console command manually

If you want to auto import it, add a cronjob to your pihole (raspberry pi) and
run this command before the gravity updates (before "pihole updateGravity" in cronjob)

    0 3   * * 7   root   wget https://blackhole.site23.de/dist/_whitelist.txt -O /etc/pihole/whitelist.txt -q > /dev/null

found this solution in:

    /etc/.pihole/gravity.sh

but for regex whitelist and blacklist it's not completed i think in pihole

### Regular Expression lists
The same like the whitelist. Import manually.

The regex blacklis is also helpful for blocking youtube ads in the browser (not in the apps).

## Other helpful stuff

with this python script there are some helpful things coming with it.
for example the "distinct-list.html" which helps you to make unique URL category lists, by filtering doubled urls out

in the "dist" folder you will also find a shell script which helps you to import the static manual lists "_[...].txt"
it downloads from a given url the static lists (see in the script) and access the pihole db to clear all values based on
the comment "__AUTOUPDATE__" and reimports the lists by the url files

for example you can run it by downloading it to your pihole and add it to a cronjob (not the same time as the gravidy update of course)

you can it like this:

    # export URL_DOMAIN="yourdomain.com" && /usr/local/bin/pihole-update-static.sh 
   

## Sources
Build the URL list based on the reports of:
* https://www.technoy.de/lists/blocklists-fuer-pihole/
* https://firebog.net/
* https://github.com/topics/pihole-blocklists


## Windows binary

The Windows binary is build with pyInstaller and can be found in the "dist" folder.
It has been build under Windows with this command:
    
    pip install pyinstaller
    pyinstaller build.py --onefile
    pyinstaller build-multi.py --onefile

### Beware ###

Some antivirus apps thinks it's a trojan in pyinstaller builded binary.
You will find some details in issues on git of pyinstaller. Maybe in future it will be fixed.


## Support it
Do you have another URL for that list or want to optimize the python script, or something else?
Just check it out, forge or do a pull request.

And don't forget to support someone else, like the people who created the URL list (see sources).