# Digital Door Sign

A digital door sign system with a web interface and display component. It is designed to be used on a Raspberry Pi with a 7" touchscreen. Fabrication files will be provided in the future.

## Features
- Web interface for status management
- Real-time status updates
- Optional text descriptions
- Time and date display
- Dark mode support
- Status management interface
- Custom color selection

## Setup
1. Clone the repository
3. Run web app: `python app.py`
4. Run display: `python display.py`

## Usage

### Web Interface
1. Access the main page at `http://localhost:5000`
2. Select a status to display
3. Add optional description text
4. Clear status when needed

### Status Management
1. Access the management page at `http://localhost:5000/manage_statuses`
2. Add new statuses with custom colors
3. Delete unwanted statuses
4. Changes are saved automatically

### Display
- Shows current status with color background
- Updates in real-time when changes are made via web interface
- Maintains time and date display
- Shows description text if provided

## File Structure

## Coming Soon
- Firebase integration
- Mobile-friendly interface
- Authentication
- Cloud hosting

## Installation

### Requirements
- Python 3.10 or higher
- Raspberry Pi (for display) or any computer for testing
- Web browser

### Setup
Clone the repository: 

## Configuration

### Status Format
Statuses are stored in `statuses.json`: 

### Display Settings
- Resolution: 800x480 (can be modified in display.py)
- Background Color: Dark theme (#1a1a1a)
- Text Color: Pure white for visibility
- Updates: Every second for time/date

## Raspberry Pi Setup

For running on Raspberry Pi:
1. Install required packages
2. Configure auto-start (optional)
3. Set up display settings
4. Prevent screen sleep

Detailed Raspberry Pi setup instructions coming soon.

## Development

Want to contribute? Here's how:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Coming Soon
- Firebase integration for cloud storage
- Authentication system
- Mobile app
- Custom themes
- Multiple display support

## Known Issues
- None currently reported

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Your Name

## Acknowledgments
- Flask for the web framework
- Pygame for the display interface
- Socket.IO for real-time communications