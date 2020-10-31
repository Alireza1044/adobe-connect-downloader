# adobe-connect-downloader
A script to download adobe connect's recorded videos from IUST's LMS system.

## Usage
- Install the latest static build of **ffmpeg** for your OS from [here](https://ffmpeg.org/download.html).
- Clone this repo:
```bash
git clone https://github.com/Alireza1044/adobe-connect-downloader.git
```
- Install the requirements:
```bash
pip install -r requirements.txt
```
- Run the program:
```bash
python main.py
```
The program asks for your LMS's username and password and link to the recorded class.
<p align="center" width="100%">
    <img width="33%" src="https://github.com/Alireza1044/adobe-connect-downloader/raw/master/p1.png"> 
</p>

**Note**: This is where you should get the link:
<p align="center">
    <img width="80%" src="https://github.com/Alireza1044/adobe-connect-downloader/raw/master/link.png"> 
</p>

- For now, You should have **Firefox** installed for the program to work. I'll try to remove this dependency in the future.

## Know issues
- If the presenter got disconnected in the middle of recording, sound and video will not be synced.
- If there was no screen share during redording(i.e. the presenter uploaded the slides to the system), There won't be any video.

If you see other issues feel free to open an issue.

## Contribution
Pull requests are welcome.
