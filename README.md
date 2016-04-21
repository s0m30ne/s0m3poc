Download the s0m3poc to your local computer and use `python s0m3poc.py` to start use it.

**Please config your account in s0m3poc.py first**:

![](http://7xp22c.com1.z0.glb.clouddn.com/note.PNG)

You can type in help to look for help.

![](http://7xp22c.com1.z0.glb.clouddn.com/help.PNG)

You can use set command to set parameters.

	If you want to search through zoomeye, you can use it just like below:
    set query <query> : to set the query you want to search through zoomeye.
    set pages <pagenum> : to set how many pages you want to serch. Default is 10.
    set facets <facets> : to set what do you want to return. Default is only IP.
    set port <True or False> : to set wehther you want to return a ip with port num, for example: 123.123.123.123:22.
        
    If you want to test for a single ip or url, you can set it like below:
    set target <target> to set the ip you want to test.
        
    set payload <payload> : select which poc file you want to use.

Use `show options` to confirm what you have configured.

![](http://7xp22c.com1.z0.glb.clouddn.com/option.PNG)

All the poc files should be found in payloads folder. You can use `show payloads` to check all the payloads you can use.

![](http://7xp22c.com1.z0.glb.clouddn.com/payloads.PNG)

`exploit` command would start to run the payload.

![](http://7xp22c.com1.z0.glb.clouddn.com/exploit.PNG)

Use `exit` to exit the program.