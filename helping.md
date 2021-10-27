### How to Help with an Issue

Because of the close relationship between the *ECHO-Cross-Program* and *ECHO_modules* repositories, addressing an issue in *ECHO-Cross-Programs* may involve also making a change to *ECHO_modules*.

1. Read through the Issues and choose one you would like to work on.
2. Ask questions for clarification by adding a comment to the issue.
3. In the upper right corner of the repository's home page look for the Fork button.  This will fork the repository into your personal Github account.
4. If you find you need to also make a change in *ECHO_modules*, also fork that repository.
6. Clone the forked ECHO-Cross-Program repository to your system, using the Code button on the repository's home page. (This should be the copy of the repository that is now in your personal account.)
7. Create an issue branch in your repository. 
   * You can do this in the Github web page for the repository, in the Code window, using the branches button (which will probably say "main".) Type in your branch name. It will say "Create branch Issue999" which you will need to click to create the new branch.
   * You can also create a branch with the git command line by entering the cloned repository folder and typing `git checkout -b Issue999`, replacing "Issue999" with an issue number and perhaps a descriptive word.
9. If you are set up to run Jupyter notebooks on your system, try to run the ECHO-Cross-Program.ipynb notebook. 
   * The first cell of the notebook will clone the ECHO_modules repository as a sub-folder of your ECHO-Cross-Program folder.
   * If you are not going to be making changes in ECHO_modules and have not forked that repository you can run the notebook as it is.
   * If you are going to make changes in ECHO_modules and have forked it, change the first line from `!git clone https://github.com/edgi-govdata-archiving/ECHO_modules.git` to `!git clone https://github.com/[your-github-id]/ECHO_modules.git -b Issue999`. I.e., change it to clone from your own ECHO_modules repository instead of "edgi-govdata-archiving", and add the "-b Issue999" (using your issue branch string).
10. If you are not set up to run Jupyter notebooks on your computer, you can use [Google's Colaboratory](https://colab.research.google.com/). This lets you run the notebook in a virtual cloud environment hosted by Google.
   * Use the Upload function and browse to the ECHO-Cross-Program.ipynb notebook file.
   * Run the code cells and make the changes to address the issue you are working on.
   * Test the notebook thoroughly.
   * When you are satisfied, first clear all output from the cells. (We don't need the output checked in with the notebook.) Use *Edit-->Clear all outputs*.
   * Save the notebook back to your system.
11. To commit your code to your respository, do these steps. (These are the steps using Github's command line.)
   * `git add ECHO-Cross-Program.ipynb`   *or the file or files you have changed*
   * `git commit -m "A brief message about the change, including the issue #11"`
   * `git push origin main`
12. You can repeat step 9 multiple times as you are working on the issue.  When you believe you have a solution that should be incorporated into the main branch:
    * Go to the repository's [Github page](https://https://github.com/[your-github-id]/ECHO-Cross-Program).  Or perhaps your change is in [ECHO_modules](https://github.com/[your-github-id]/ECHO_modules). Or you may have made changes to both repositories.
    * Look for your branch under the list of *branches*.
    * Click on the *New Pull Request* button for your branch.  Add some description of the change.
    * We will review and test your change. If all goes well, we'll merge it into the *main* branch of the repository.
