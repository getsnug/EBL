# EBL Made Easy
## Preface:
Hello, this codebase is for the purpose of being able to perform Electron Beam Lithography(EBL) an a ThermoFisher desktop SEM, using the pyPhenom ppi interface. Given that most universities have access to an SEM it seems limiting that the programs to perform EBL are not widely available. My goal with this project is to make EBL accessible to anyone with access to an SEM. I'm not super sure who initially wrote the code at ThermoFisher but a huge thanks to them for setting this up. Also, for the duration of this project I will be using this document as a way to keep track of troubleshooting our procedure.
## Getting Started:
To start I have made [this spreadsheet](https://docs.google.com/spreadsheets/d/1bMO-lNjuLOMj197D0d5k7s-SDoznpCuAyAkXTVNEcZo/edit?usp=sharing). This will be the main document where you enter your EBL parameters, there is a column for filenames, where you will put the .png files that you wish to etch(each filename must be in quotes: "file.png"). Then you enter your dwell times, this is how long the SEM will trace the pattern for. There are two columns for size, please see the size table in order to pick a size. And finally there are two columns for increments, these decide the spacing of your patterns on the grid. Once you've entered your desired values, put all of your images, along with your spreadsheet(saved as main.csv) into a folder. Here I have all mine in a directory called images<img width="667" alt="Screenshot 2023-11-03 at 2 17 02 PM" src="https://github.com/getsnug/EBL/assets/16107813/eb4995fa-6298-46b7-b38c-371672fbad4c">

Once you've got your images and control file in a folder, you need only make sure your directory is entered it BitmapScan.py like here:<img width="871" alt="Screenshot 2023-11-03 at 2 01 41 PM" src="https://github.com/getsnug/EBL/assets/16107813/23a471f8-3e7c-49f1-a3e1-d4c6ed683db7"> 


You'll notice that there is also an option for a logFileName, this log file will save all of your outputs, it should look very similar to the input spreadsheet except that it will also have position values for each pattern. Finally there is an offset parameter, read more about our process to understand what the offset parameter means.
That's it. You're ready to EBL, if you're chip is ready pop it in to the SEM and start etching!
## Process:
### Preface:
Here I will describe our process, this will likely look different depending on your application, but for our labs purposes, as well as anyone starting without much direction this should be a good starting point.
### Making the chip:
We start with either a silicon or ITO chip and spin coat it with PMMA A6 at 4500 rpm for 30 seconds. Make sure you give it enough time to spin out the bubbles as it starts. After spin coating we bake the chip on a heat plate at $200^{\circ}$ Celcius for at least one minute.
After spin coating we scratch a 'scarecrow' into the chip. This is how we will orient ourselves when we look at the chip under the SEM.
# Insert Image of Scratch and Explain
### Etching:
Now we make sure our chip is clean and pop it in the SEM, we find the scratch with the optical microscope, but we can really find the top once we've entered the SEM. Once you've aligned yourself with the top of the scratch you're good to go. Press run on the program and sit back while it etches.

After your chip is done in the SEM its time to develop it. We develop ours in isopropyl alchohol for around 10-20 seconds, before stopping the reaction with water. If you take the chip out and it looks under developed no worries, you can just give it a few more seconds of isopropyl. You should be able to see your patterns almost as a diffraction grating on the chip after development. Here you may also check the quality of your sample under an AFM or optical microscope. DO NOT try to look at it under the SEM until you've finished it, this will etch away the rest of the PMMA.
### Finishing:
We are conducting plasmonics research so we finish our chips in aluminum by sputtering for 1-4 minutes. This is it, we lift off with acetone or tape and then observe our samples. I'll include some issues that we're seeing at the moment in the next section. Feel free to reach out to me at vaughngramsey@gmail.com if you have any questions or suggestions.
