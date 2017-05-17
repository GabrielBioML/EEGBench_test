Here's the code line to setup your PI for github. It sets
the connexion to github after you have created 
your repository

1. Be sure to have SSH enabled

2. Check if you have existing SSH keys

	ls ~/.ssh 
	#Lists the existing keys .ssh directory. 
	They should appear in .pub
	if there's none go to step 3 and if you have one
	go to step 4
3. Generating a new SSH key

	ssh-keygen -t rsa -b 4096 -c "your_email@example.com"
	#This creates a neww ssh key
	Then, press enter (3 times) to set the 3 settings 
	to default

	eval $(ssh-agent -s) #This start the ssh agent in
	the background.

	ssh-add ~/.ssh/id_rsa #This add the key to your 
	key file
	
4. Add the SSH key to your GitHub
	
	cat < ~/.ssh/id_rsa.pub #This shows your key code.
	Copy it

	In your GitHub, go in SETTIGNS, select SSH and	
	GPG keys. Then, click new SSH key or Add SSH key

	Tile = name_of_your_device
	
	Paste your key code in into the key field. 
	Click Add SSH key.

5. Confirm that the connexion has been established
	
	ssh -T git@github.com #Attempts to SSH to GitHub
	
	You will received the following message:
	Hi username! You've successfully authentificated,
	but GitHub does not provide shell access.

	You are linked with your GitHub account!


	