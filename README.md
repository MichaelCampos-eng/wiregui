<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][LICENCE.txt]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">NeXport</h3>

  <p align="center">
    Wire manager GUI that maps connections and connectors for DITMCO testing.  
    <br />
    <a href="https://github.com/MichaelCampos-eng/wiregui.git"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MichaelCampos-eng/wiregui.git">View Demo</a>
    &middot;
    <a href="https://github.com/MichaelCampos-eng/wiregui.git/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/MichaelCampos-eng/wiregui.git/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started. To avoid retyping too much info, do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`, `project_license`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![PyQt6][PyQt]][PyQt6.com]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The package requires several main stream packages as well as a custom library. A YAML file for conda env
creation and TOML file for packages installion help 

### Prerequisites

Install git for Windows [https://git-scm.com/downloads/win]

* Git installation using Powershell
  ```sh
  winget install --id Git.Git -e --source winget
  ```

Install miniconda for Windows, other OS or more detailed instructions found at [https://docs.anaconda.com/miniconda/install/]
* Miniconda for Windows
  ```sh
  curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
  start /wait "" .\miniconda.exe /S
  del .\miniconda.exe
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MichaelCampos-eng/wiregui
   ```
3. Create a new environment with package prerequisites at root project
   ```sh
   conda env create -f environment.yaml
   ```
4. Download dependencies at root project
   ```sh
   pip install .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run the gui, open the anaconda terminal prompt and run `start.py`

  ```sh
  python start.py
  ```

For each table shown, the user input text boxes show the format the user need to follow.

  1. Wire List: 
    a. 'FROM' (SPACE) 'PIN' correlates to typing in reference designator followed by space followed by pin, press enter when complete
    b. 'TO' (SPACE) 'PIN' correlates to typing in reference designator followed by space followed by pin, press enter when complete
  
  2. Unused List: 'REF DES' (SPACE) 'PIN' correlates to typing in reference designator followed by space followed by pin, press enter when complete

  3. Ground List:
    a. "Connector" correlates to typing in the harness/adapter reference designator, press enter when complete
    b. "Ground" correlates to typing in associated ground reference designator, press enter when complete

To remove an entry from list, type REMOVE 'INDEX_NUMBER'

There a 3 tab menus: File, Import, Export

1) File
  a. Open
    i. 'Open Project' feature that opens file (.tb) containing all list and image schematic data
    ii. 'Open Document' feature that opens schematic (.pdf)
    iii. 'Open image' idle feature that opens schematic (.png)
2) Import
  a. Spreadsheet
    i. 'Wire List' opens csv file with appropriate column names and displays it on table
    ii. 'Unused List' opens csv file with appropriate column names and displays it on table
    iii. 'Ground list' opens csv file with appropriate column names and displays it on table
3) Export
  a. Spreadsheet
    i. 'Wire List' saves csv file
    ii. 'Unused List' saves csv file
    iii. 'Ground list' saves csv file
    iv. 'All' saves all lists as csvs in a directory
  b. Test
    i. 'Wire List' creates test script for list
    ii. 'Unused List' creates test script for list
    iii. 'Ground list' creates test script for list
    iv. 'All' creates a single test script for all lists

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [X] Data transfer
    - [X] Export/Import spreadsheets
    - [X] Export custom DITMCO test scripts
- [ ] List Management
    - [X] Append/Remove to entries
    - [X] Duplicate handling
    - [ ] In-place entry manipulation
- [ ] Wire Detection
    - [X] Import and convert pdf schematic to image
    - [ ] Detect wire connections
    - [ ] Maps pins to reference designators
    - [ ] Appends connector-pin to wire list upon clicking on wire
- [ ] Automated Net List Creation
    - [ ] Implementation of object detection to identify all components and location
    - [ ] With wire detection, automatically map all connector-pins 

See the [open issues](https://github.com/MichaelCampos-eng/wiregui.git/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/WireGui`)
3. Commit your Changes (`git commit -m 'Add some WireGui'`)
4. Push to the Branch (`git push origin feature/WireGui`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Michael Campos - michael_C55@berkeley.edu

Project Link: [https://github.com/MichaelCampos-eng/wiregui.git](https://github.com/MichaelCampos-eng/wiregui.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[PyQt6]: https://img.shields.io/pypi/pyversions/:packageName
[PyQt6.com]: https://doc.qt.io/qtforpython-6/

