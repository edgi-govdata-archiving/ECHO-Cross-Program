### How to Help with an Issue

Because of the close relationship between the *ECHO-Cross-Program* and *ECHO_modules* repositories, addressing an issue in *ECHO-Cross-Programs* may involve also making a change to *ECHO_modules*.

1. Read through the Issues and choose one you would like to work on.
2. Ask questions for clarification by adding a comment to the issue.
3. Create a branch with a descriptive name, including the issue number, e.g. #11, in the name.  It could be *steves-branch #11*.
4. If you find you need to also make a change in *ECHO_modules*, create a branch in that repository with the same name.
5. Clone the repository to your system, using the Code button on the repository's home page.
6. Change your local copy of the repository to the branch you created.  (On the command line you can see what branch you are on by the 'git status' command.  The command 'git checkout mybranch' will switch to the mybranch branch.)
7. If you are set up to run Jupyter notebooks on your system, try to run the ECHO-Cross-Program.ipynb notebook. 
8. If you are not set up to run notebooks, you can use [Google's Colaboratory](https://colab.research.google.com/). This lets you run the notebook in a virtual cloud environment hosted by Google.
   * Use the Upload function and browse to the ECHO-Cross-Program.ipynb notebook file.
   * Run the code cells and make the changes to address the issue you are working on.
   * Test the notebook thoroughly.
   * When you are satisfied, first clear all output from the cells. (We don't need the output checked in with the notebook.) Use *Edit-->Clear all outputs*.
   * Save the notebook back to your system.
9. To commit your code to your branch in the respository, do these steps. (These are the steps using Github's command line.)
   * git add ECHO-Cross-Program.ipynb   *or the file or files you have changed*
   * git commit -m "A brief message about the change, including the issue #11"
   * git push origin steves-branch #11
