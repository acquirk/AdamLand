# BigPicture

BigPicture is a minimalist project management app designed for solopreneurs and generalists. It provides a holistic approach to managing various aspects of life and work through a simple, intuitive interface.

## Overview

BigPicture organizes your life and projects into four main categories, called "Buckets":

1. **Internal**: For personal development projects (e.g., health plans, philosophical explorations, habit formation)
2. **Home**: For daily life management (e.g., budgeting, taxes, home repairs, vehicle maintenance)
3. **Family**: For relationship-related projects and goals
4. **External**: For projects to be shared with society (e.g., woodworking, art, writing, business ideas)

Each Bucket contains multiple Projects, and each Project can have multiple Goals, checklists, text areas, and URLs.

## Features

- Four pre-defined Buckets with customizable subtitles and advice
- Create and manage multiple Projects within each Bucket
- Add Goals to Projects with deadlines
- Integrate with Google Calendar or iCal for deadline tracking
- Minimalist and intuitive user interface
- Checklist functionality for tracking progress
- Text areas for additional notes and information
- URL storage for relevant links and resources

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Flask-WTF

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bigpicture.git
   cd bigpicture
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   python create_db.py
   ```

4. Run the application:
   ```
   flask run
   ```

5. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Upon first launch, you'll see the four pre-defined Buckets.
2. Click on a Bucket to view its Projects.
3. Add a new Project by entering a name in the "Add a project" field.
4. Within a Project, add Goals using the "Add a goal" field.
5. Use the provided text areas for additional notes or information.
6. Add relevant URLs to your Projects for easy reference.

## Contributing

We welcome contributions to BigPicture! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

Your Name - your.email@example.com

Project Link: https://github.com/yourusername/bigpicture
