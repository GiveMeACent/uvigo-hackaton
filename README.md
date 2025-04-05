**Requirements. User Stories.**  
**User Stories for the Camera Management and Data Processing System**

### Tasks related to camera connection and configuration:

#### Automatic detection of supported cameras:

As a user, I want the system to automatically recognize when I connect a supported USB camera so that I don't have to manually configure the camera every time I connect it.  
**Acceptance Criteria:**

- The system automatically detects cameras whose identifiers are listed in the configuration file.
- Logs are generated when a supported camera is connected, indicating that the device has been recognized correctly.

#### Management of unsupported cameras:

As a user, I want the system to continue running without errors when I connect an unsupported camera to avoid execution issues.  
**Acceptance Criteria:**

- The system displays a message indicating that the camera is not supported.
- Processes already running are not interrupted due to the connection of an unsupported camera.

#### Automatic creation of folder structures:

As a user, I want the system to automatically create the necessary folder structures when a supported camera is connected, to properly organize the downloaded data.  
**Acceptance Criteria:**

- Folders are created in a configurable location defined in the configuration file.
- The structure includes subfolders for videos and GCSV files.

#### Automatic process start upon camera connection:

As a user, I want the download and management process to automatically start when I connect a supported camera, so I don't have to manually start the system.  
**Acceptance Criteria:**

- The system automatically starts downloading videos and GCSV files as soon as a supported camera is detected.
- No user intervention is required after connecting the camera.

#### Video download from camera:

As a user, I want the system to automatically download all videos stored in the camera upon connection to efficiently store my content.  
**Acceptance Criteria:**

- All videos in the camera are successfully downloaded to the assigned folder.
- Logs of the downloaded videos are generated.

#### Prevent overwriting existing videos:

As a user, I want videos that have already been downloaded not to be downloaded again or overwritten, to avoid unnecessary duplicates.  
**Acceptance Criteria:**

- The system verifies if a video already exists in the folder before downloading it.
- Existing videos are not overwritten, and duplicates are ignored.

#### Download associated GCSV files:

As a user, I want the system to automatically download GCSV files associated with each video using the same name as the original video, to keep all data synchronized.  
**Acceptance Criteria:**

- Each GCSV file is downloaded along with its corresponding video using the same name.
- If the GCSV file already exists, it is not downloaded again.

#### Download missing GCSV files:

As a user, I want the system to download GCSV files that may be missing for already downloaded videos to ensure the information is complete.  
**Acceptance Criteria:**

- The system automatically detects missing GCSV files and downloads them.
- Logs are generated indicating the GCSV files that were downloaded.

#### Configuration of supported cameras:

As a user, I want to define the identifiers of supported cameras in a configuration file to easily add support for new cameras.  
**Acceptance Criteria:**

- The configuration file allows adding or modifying identifiers of supported cameras.
- The system recognizes newly added cameras after the configuration file is updated.

#### System execution with a single command:

As a user, I want to initialize the system with a single command in the terminal so that it runs indefinitely, avoiding complex executions.  
**Acceptance Criteria:**

- The system runs indefinitely with a single command.
- Manual restarts are not required to manage new camera connections.

#### Well-structured and documented code:

As a developer, I want the code to be structured in a readable manner and to have clear and complete documentation to facilitate maintenance and comprehension.  
**Acceptance Criteria:**

- The code structure follows clear design patterns.
- The documentation includes details about the implementation, configuration, and use of the system.

#### Innovative solution for camera management:

As a developer, I want the code to implement an original and innovative solution to optimize the system's functionalities.  
**Acceptance Criteria:**

- The code introduces unique mechanisms for managing cameras and synchronizing data.
- The system's functionalities surpass standard solutions in the market.

---

### Tasks related to data transformation:

#### One-step data transformation:

As a user, I want to execute a script that performs all relevant data transformations to automatically generate processed content from the video and GCSV file.  
**Acceptance Criteria:**

- The script transforms videos and data with a single command.
- A folder with processed data is created after the script execution.

#### Creation of configurable folders:

As a user, I want the script to automatically generate a folder named after the video in a configurable path to organize the generated data.  
**Acceptance Criteria:**

- The folder path is defined in the configuration file.
- The folder includes subfiles for videos, audio, and synchronized data.

#### Extraction of audio in WAV format:

As a user, I want the system to generate a WAV file with the audio from the video to have the audio available independently.  
**Acceptance Criteria:**

- The WAV file is generated with the audio quality of the original video.
- The file name matches the processed video name.

#### Synchronization of GCSV data and video:

As a user, I want a synchronized file that relates GCSV data to each video frame to facilitate data analysis.  
**Acceptance Criteria:**

- The synchronized file includes acceleration and orientation data per frame.
- Synchronization is tested across multiple videos to ensure accuracy.

#### Stabilized video generation:

As a user, I want the system to generate a new stabilized video using data from the GCSV file to improve the quality of the processed content.  
**Acceptance Criteria:**

- The stabilized video uses gyroscope data to eliminate vibrations.
- Results are evaluated to verify visual improvements.

#### Overlaying accelerometer and gyroscope data:

As a user, I want the system to incorporate accelerometer and gyroscope data over the stabilized video to dynamically visualize that information.  
**Acceptance Criteria:**

- Accelerometer and gyroscope data are displayed on the video in real-time.
- The overlay is clear and does not interfere with video visualization.

---

### Tasks related to video segment selection:

#### Creation of a video with selected segments:

As a user, I want a script to generate a new video composed of three 5-second segments from the previously processed video to summarize relevant content.  
**Acceptance Criteria:**

- The resulting video contains three specific segments of 5 seconds each.
- The selected segments are based on their assigned score.

#### Scoring based on defined parameters:

As a user, I want the script to assign scores to segments based on defined parameters to automatically select the best parts.  
**Acceptance Criteria:**

- Segments are scored based on criteria such as sudden braking, visible cars, and people speaking.
- Scores are displayed in the script's logs.

#### Optimization of selection without overlap:

As a user, I want the script to select segments maximizing scores while ensuring no overlap between them to obtain a clear and diverse result.  
**Acceptance Criteria:**

- Selected segments do not share common seconds.
- The algorithm prioritizes higher scores while ensuring diversity.

#### Progress indicator during processing:

As a user, I want the script to display a clear progress indicator while the video is being processed to keep me informed in real time.  
**Acceptance Criteria:**

- Progress is displayed as a percentage or the number of segments processed.
- The script's interface does not freeze during execution.
