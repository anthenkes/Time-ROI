# Productivity and ROI Tracker

## Description
This simple desktop application is designed to help you track the time you spend on various tasks and evaluate their ROI (Return on Investment) based on four metrics. By assessing each task's immediate benefits, future impact, personal fulfillment, and progress, this tool gives you insights into which activities provide the most value for your time.
Features

  Track and categorize activities by their time investment.
  Score activities across multiple criteria: immediate benefit, future impact, personal fulfillment, and quantity of progress made.
  Calculate average output scores and ROI for each task, helping you to prioritize high-impact activities.


## Features

- **Task Logging**: Log tasks with details such as date, category, time investment, start time, end time, immediate benefit, future impact, personal fulfillment, progress, and notes.
- **ROI Calculation**: Automatically calculates the ROI for each task based on the provided metrics.
- **Form Submission**: Submit tasks using the submit button or the `Ctrl+Enter` keyboard shortcut.
- **Toast Notifications**: Displays toast notifications for successful task submissions.
- **Error Handling**: Displays error messages in a pop-up if task submission fails.

## Installation

1. **Clone the Repository**:
```
   git clone https://github.com/anthenkes/Time-ROI.git
   cd Time-ROI
```
3. **Create Virtual Environment**
```
  python -m venv env
  source env/bin/activate # On Windoes, use 'env/Scripts/activate'
```
4. **Install Dependencies**
```
  pip install -r requirements.txt
```

## Usage
1. **Run the Application**
   (while in the root folder of the project)
```
  python run.py
```
2. **Logging a Task**
   - Fill in the task details in the form.
   - Press the Submit button or use the `Ctrl+Enter` keyboard shortcut to submit the form.
3. **View Notifications**
    - A toast notification will appear at the top of the application to confirm successful task submission.
    - If there is an error, a pop-up will display the error message.

## Task Metrics
- Immediate Benefit: Rate the immediate benefit of the task on a scale of 0 to 5.
- Future Impact: Rate the future impact of the task on a scale of 0 to 5.
- Personal Fulfillment: Rate the personal fulfillment of the task on a scale of 0 to 5.
- Progress: Enter the progress of the task as a percentage (0 to 100). The application will normalize this value to a scale of 1 to 5.

## ROI Calculation
The ROI for each task is calculated using the following formulas:

 ```
Output Score = metrics / total number of metrics
ROI = Output Score / Time Investment (in hrs)
```
Where the Output Score is the average of the immediate benefit, future impact, personal fulfillment, and normalized quantity of progress.

## Example Task

**Task**: Practicing Piano

- **Time Investment**: 30 minutes
- **Immediate Benefit**: 2
- **Future Impact**: 3
- **Personal Fulfillment**: 5
- **Quantity of Progress Made**: 4 (around 70% of learning a new scale)

### Average Output Score
The average output score is calculated as:

Average Output Score = (2 + 3 + 5 + 4) / 4 = 3.5

### ROI Calculation
For 30 minutes (0.5 hours) of piano practice:

ROI = 3.5 / 0.5 = 7.0

## Project Structure
```
Time-ROI/
│
├── backend/
│   ├── data/
│   │   ├── dbmanager.py
│   │   ├── dbSetUp.py
│   │   └── task_log.db
│   ├── logs/
│   │   └── logger_setup.py
│   └── __init__.py
│
├── frontend/
│   ├── main.py
│   └── __init__.py
│
├── models/
│   ├── task.py
│   └── __init__.py
│
├── run.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or inquiries, please contact anthonyhenkes@gmail.com.



### Explanation

1. **Features**: Describes the main features of the application.
2. **Installation**: Provides step-by-step instructions for setting up the application.
3. **Usage**: Explains how to run the application and log tasks.
4. **Task Metrics**: Describes the metrics used for logging tasks.
5. **ROI Calculation**: Explains how the ROI is calculated.
6. **Example Task**: Gives and example of how the ROI is calculated.
7. **Project Structure**: Provides an overview of the project structure.
8. **Contributing**: Encourages contributions and provides guidelines.
9. **License**: Specifies the license for the project.
10. **Contact**: Provides contact information for inquiries.

Feel free to customize the README file as needed to better fit your project.


