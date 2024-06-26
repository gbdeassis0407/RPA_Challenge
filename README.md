# News Site Data Extraction Bot

## Overview

Our mission is to enable all people to do the best work of their lives—the first act in achieving that mission is to help companies automate tedious but critical business processes. This RPA challenge showcases the ability to build a bot for purposes of process automation.

## 🟢 The Challenge

This challenge involves automating the process of extracting data from a news site.

You should push your code to a **public** Github repo, and then use that repo to [create a Robocorp Control Room process](https://robocorp.com/docs/courses/beginners-course-python/12-running-in-robocorp-cloud). The process should have a completed successful run before submission. Make sure to [write your files to the `/output` directory](https://robocorp.com/docs/courses/beginners-course-python/9-collecting-the-results#saving-the-file-to-the-output-directory) so that they are visible in the artifacts list.

### The Source

You are free to choose from any general news website. Some examples include:

- [AP News](https://apnews.com/)
- [Al Jazeera](https://www.aljazeera.com/)
- [Reuters](https://www.reuters.com/)
- [Gothamist](https://gothamist.com/)
- [LA Times](https://www.latimes.com/)
- [Yahoo News](https://news.yahoo.com/)

### Parameters

The process must handle three parameters via the Robocorp work item:

- **Search Phrase**
- **News Category/Section/Topic**
- **Number of Months for which you need to receive news**

    Example: 
    - 0 or 1 - only the current month
    - 2 - current and previous month
    - 3 - current and two previous months, and so on

These parameters can be defined within a configuration file but should ideally be provided via a [Robocloud workitem](https://rpaframework.org/libraries/robocorp_workitems/).

### The Process

The main steps:

1. Open the news site.
2. Enter the search phrase in the search field.
3. On the results page:
    - If possible, select a news category or section.
    - Choose the latest (i.e., newest) news.
4. Extract the following values:
    - Title
    - Date
    - Description
5. Store the extracted data in an Excel file:
    - Title
    - Date
    - Description (if available)
    - Picture filename
    - Count of search phrases in the title and description
    - Boolean indicating whether the title or description contains any amount of money
6. Download the news picture and specify the file name in the Excel file.
7. Repeat steps 4-6 for all news that falls within the required time period.

### Submission Checklist

1. **Quality Code**: Ensure your code is clean, maintainable, and well-architected. Follow [PEP8 compliance](https://peps.python.org/pep-0008/) and employ [OOP principles](https://peps.python.org/pep-0008/).
2. **Resiliency**: Ensure your architecture is fault-tolerant and can handle failures at both the application and website levels. Utilize [explicit waits](https://selenium-python.readthedocs.io/waits.html) and the [Robocorp wrapper browser for Selenium](https://rpaframework.org/libraries/browser_selenium/python.html).
3. **Best Practices**: Follow best RPA practices. Use proper [logging](https://docs.python.org/3/library/logging.html) and appropriate [string formatting](https://www.digitalocean.com/community/tutorials/python-string-concatenation) in your logs (Python 3.8+).

## Getting Started

### Prerequisites

- Python 3.8+
- Robocorp Lab or Robocorp Code
- Required Python libraries (specified in requirements.txt)

### Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/gbdeassis0407/RPA_Challenge.git
  ```
  2. Install the required libraries:
  - Copiar código
  ```sh
  pip install -r requirements.txt
  ```
## Usage
  Set up your Robocorp Control Room process following this guide.
  Define the parameters in a Robocloud work item.
- Run the process.
- Output
- The extracted data will be stored in an Excel file in the /output directory, along with the downloaded news pictures.