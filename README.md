# INFO 5940 
Welcome to the INFO 5940 repository. You will complete your work using [**GitHub Codespaces**](#about-github-codespaces) and save your progress in your own GitHub repository. This guide will walk you through setting up the development environment and running the test notebook.  

## Getting Started 

### Step 1: Fork this repository 
1. Click the **Fork** button (top right of this page).
2. This will create a copy of the repo under **your own GitHub account**.

Forking creates a personal copy of the repo under **your** GitHub account.  
- You can commit, push, and experiment freely.  
- Your work stays separate from the official class materials.

### Step 2: Open your forked repo Codespace
1. Go to **your forked repo**.
2. Click the green **Code** button and switch to the **Codespaces** tab.  
3. Select **Create Codespace**.
4. Wait a few minutes for the environment to finish setting up.

### Step 3: Verify your environment 
Once the Codespace is ready: 
1. If you are in `<your-file-name>.ipynb` in your codespace.
2. Install the Python 3.11.13 Kernel.  In the top-right corner, click **Select Kernel**.
    1. If **Install/Enable suggested extensions Python + Jupyter** appears, select it, and wait for the install to finish before moving on to the next step.
    2. Select **Python Environments** choose **Python 3.11.13 (first option)**.
3. Run the code block to check your setup. 

## About GitHub Codespaces

[Codespaces](https://docs.github.com/en/codespaces) is a complete software development and execution environment, running in the cloud, with its primary interface being a VSCode instance running in your browser.

Codespaces is not free, but their per-month [free quota](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces#free-quota) is generous.  Codespaces is free under the [GitHub Student Developer Pack](https://education.github.com/pack#github-codespaces).

### Codespaces Tips

* Codespaces keep running even when you close your browser (but will time out and stop after a while)
* Unless you're on a free plan, or within your free quota, costs acrue while the codespace is running, whether or not you have it open in your browser or are working on it
* You can control when it's running, and the space it takes up.  Check out [GitHub's codespaces lifecycle documentation](https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle)

## Sync Updates 
To make sure your personal forked repository stays up to date with the original class repository, please follow these steps:
1. Open your forked repo.
2. At the top of the page, you should see a banner or menu option that shows whether your fork is behind the original repo.
3. Click the **Sync fork** button.
4. In the dropdown, choose **Update branch** to pull the latest changes from the original repo into your fork.

Optionally, you can also follow these steps to create a new branch on your fork:
1. Open your **forked repository** on GitHub.  
2. At the top of the page, next to the branch dropdown, click the **Branches** button.  
3. In the **Branches** view, click the green **New Branch** button.  
4. In the popup window, enter a branch name.  
   - You can use any name you like, but it’s recommended to match the branch name used in class for better organization.  
5. Under **Branch source**, select:  
   - **Repository:** `AyhamB/INFO-5940-Codespace`  
   - **Branch:** choose the branch you want to sync from (e.g., `streamlit`).  
6. Click the green **Create New Branch** button.  
7. Verify that you’re now back in **your fork**, on the new branch you just created.  
8. Click the **Code** button and create a new Codespace (if you don’t already have one).  
   - Make sure the Codespace is created from the **current branch**.
  
## Running a Streamlit App on Codespaces  
Follow these steps to launch and view your Streamlit app in GitHub Codespaces:
1. **Open the terminal** inside your Codespace.
2. Run the command:  
   ```bash
   streamlit run your-file-name.py
   ```  
   **(Replace `your-file-name.py` with the actual name of your Streamlit app file, e.g., `hello_app.py`.)**
3. After pressing **Enter**, a popup should appear in the bottom-right corner of Codespace editor.  
   - Click **“Open in Browser”** to view your app.  

   ⚠️ *If you miss the popup:*  
   - Press **Ctrl + C** in the terminal to stop the app.  
   - Rerun the command from step 2 — the popup should appear again.
4. A new browser tab will open, showing the interface of your Streamlit app.
5. **Make changes to your code** in the Codespace editor.  
   - Refresh the browser tab to see the updated version of your app.  

## Setting Your API Key in GH Codespaces
You will receive an individual API Key for class assignments. To prevent accidental exposure online, please follow the steps below to securely insert your key in the terminal.
1. **Open the terminal** inside your Codespace.
2. Run the command to temporarily set your API Key for this session:  
   ```bash
   export API_KEY="your_actual_API_KEY"
   ```
3. If you want to run the Streamlit app and set up the key at the same time, run both commands together:
   ```bash
   API_KEY="your_actual_API_KEY" streamlit run your-file-name.py
   ```

## Multi-file question answering system

### Overview
Allows user to upload multiple pdf and txt and then ask questions about them. Uses APIs, Streamlit, LangChain, and Chromadb to power the system. 

Covers:
- Utilize the Provided Codespace Setup
- File Upload Functionality for .txt Files
- RAG System and Conversational Interface. Including Document Ingestion and Chunking, Retrieval-Augmented Generation, Conversational Interface
- Support for .txt and .pdf File Formats
- Ability to Add Multiple Documents

### To Run:

Open codespaces. 

Then install requirements
   ```bash
   pip install -r requirements.txt
   ```

Provide API key and run application
   ```bash
   API_KEY="your-key" streamlit run chat_with_pdf.py
   ```
 
The chat will be available in localhost, usually at `http://localhost:8501`

To use the application:
First upload documents (txt or pdf) and then ask question about the documents in the chat feature at the bottom. 
If desired remove documents indivually of clear all the documents. Also, sources will get cited in the answer. 

### Technical Aspects
The user interface is powered by Streamlit which the connects to the backend to handle the documents. In the backend, the documents are uploaded, chunked, embedding are created, and vector similarity is channeled. For the RAG pipeline the user asks questions, then similarity search with top 5 chunks and producing answers via the API. 

Chunking as per industry standards are 1000 character chunks, 250 character overlap, and use of 5 top chunks per similarity. In answers, sources will be provided. 

### Changes to configurations
**`requirements.txt`** dependencies added to power the system 



