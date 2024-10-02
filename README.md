![Tests](https://github.com/BeNeuroLab/beneuro_experimental_data_organization/actions/workflows/run_tests.yml/badge.svg)

This is a collection of functions for managing the experimental data recorded in the 
BeNeuro Lab, and a CLI tool called `bnd` for easy access to this functionality.

# Pipeline
The intended pipeline of use of `bnd` is as follows:

After you recorded an experimental session in the lab PCs:
```shell
# From the lab PC
$ bnd up MXX  # Uploads latest session of animal MXX to RDS
```
On your local PC:
```shell
$ bnd dl MXX  # Download latest session of animal MXX from RDS to local PC
$ bnd kilosort-session MXX_2024_01_01_09_00  # Kilosorts session and saves in local processed
$ bnd to-nwb MXX_2024_01_01_09_00  # Converts data to .nwb format
$ bnd nwb-to-pyaldata MXX_2024_01_01_09_00  # Convert session into pyaldata format
$ bnd up MXX_2024_01_01_09_00  # Still pending. Uploads nwb and pyaldata to rds processed
```
# Setting up
## Installation
1. You will need the environment management tool [poetry](https://python-poetry.org). We 
   recommend using the official installer:
    - On Linux, MacOS or WSL:
        ```shell
        $ curl -sSL https://install.python-poetry.org | python3 -
        ```
    - On Windows Powershell: 
        ```shell
        $ (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
        ```
      - You may need to add poetry to $PATH environment variable

   
2. Clone this repo:
   ```shell
   $ git clone https://github.com/BeNeuroLab/beneuro_experimental_data_organization.git
   ```

3. Navigate into the folder you just downloaded (`beneuro_experimental_data_organization`)
4. Create the environment associated to the project: `poetry shell`. This will generate a 
   virtualenv where you install all the packages needed for `bnd` and activate it
5. Install the package with either `poetry install` or if you want processing 
   functionality: `poetry install --with processing`. For more info, see the [spike 
   sorting instructions](#spike-sorting).

6. Test that the installation worked with: `poetry run pytest`. Hopefully you'll see 
   green on the bottom (some yellow is fine) meaning that all tests pass :)


> Note:
>
> If you want to make the environment activation a bit more straightforward instead of 
> navigating to the folder and running `poetry shell` you can make an alias in your 
> terminal app:
> - Windows:
>   ```shell
>   # Open PowerShell as admin
>   $ notepad C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
>   ```
>   Edit the file, add the following, and save it in the folder
>   ```text
>   function ActivatePoetryBnd {
>    & " \path\to\your\project\Scripts\activate"
>   }
>   Set-Alias activate_bnd ActivatePoetryBnd
>   $ alias activate_bnd='source /path/to/your/project/.venv/bin/activate'
>   ```
>   Close the file and go back to powershell and run
>   ```shell
>   $ activate_bnd
>   ```
> - Linux:
>   ```shell
>   $ nano ~/.bashrc # or vim ~./bashrc
>   $ alias activate_bnd='source /path/to/your/project/.venv/bin/activate'
>   ```


## Configuring the local and remote data storage
The tool needs to know where the experimental data is stored locally and remotely.

0. Mount the RDS server. (If you're able to access the data on it from the file browser, it's probably already mounted.)

1. Run `bnd init` and enter the root folders where the experimental data are stored on the local computer and the server. These refer to the folders where you have `raw` and `processed` folders.

   This will create a file called `.env` in the `beneuro_experimental_data_organization` folder and add the following content:
   ```
   LOCAL_PATH = /path/to/the/root/of/the/experimental/data/storage/on/the/local/computer
   REMOTE_PATH = /path/to/the/root/of/the/experimental/data/storage/where/you/mounted/RDS/to
   ```

   Alternatively, you can create this file by hand.

2. Run `bnd check-config` to verify that the folders in the config have the expected `raw` and `processed` folders within them.


# CLI usage
## Help
- To see the available commands: `bnd --help`
- To see the help of a command (e.g. `rename-videos`): `bnd rename-videos --help`

## Uploading the data
Once you're done recording a session, you can upload that session to the server with:
  
  `bnd up <subject-name-or-session-name>`

This should first rename the videos and extra files (unless otherwise specified), validate the data, then copy it to the server, and complain if it's already there.

## Downloading data from the server
Downloading data to your local computer is similar to uploading, but instead of throwing errors, missing or invalid data is handled by skipping it and warning about it.

Using the session's path assuming you have RDS mounted to your computer:

  `bnd dl <subject-name-or-session-name>`

## Spike sorting
Currently we are using Kilosort 4 for spike sorting, and provide a command to run sorting on a session and save the results in the processed folder.

Note that you will need some extra dependencies that are not installed by default, and that this will most likely only work on Linux.<br>
You can install the spike sorting dependencies by running `poetry install --with processing` in bnd's root folder.

You will also need docker to run the pre-packaged Kilosort docker images and the nvidia-container-toolkit to allow those images to use the GPU.<br>
If not already installed, install docker following the instructions [on this page](https://docs.docker.com/engine/install/ubuntu/), then install nvidia-container-toolkit following [these instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).


Basic usage:

  `bnd kilosort-session . M020`

Only sorting specific probes:

  `bnd kilosort-session . M020 imec0`

  `bnd kilosort-session . M020 imec0 imec1`

Keeping binary files useful for Phy:

  `bnd kilosort-session . M020 --keep-temp-files`

Suppressing output:

  `bnd kilosort-session . M020 --no-verbose`

# Please file an issue if something doesn't work or is just annoying to use!
