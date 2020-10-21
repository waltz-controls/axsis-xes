[![time tracker](https://wakatime.com/badge/github/Ingvord/axsis-xes.svg)](https://wakatime.com/badge/github/Ingvord/axsis-xes)

# AXSIS XES spectrometer

Requires [libpi_pi_gcs2_x86_64]() from PI CD and [PIPython](https://github.com/git-anonymous/PIPython)

## How to run

Assuming all dependencies are installed.

On Windows:

To start back-end, run sequentially in project root folder:

1. `set FLASK_APP=axsis.py`

2. `set MODE=production`  OR `set MODE=simulation`

3. `flask run`

To start front-end (gui)

1. `npm run start` - ensure to run from *gui* folder
