# git-mirroring-py
Python script to mirror git repositories hosted on GitHub to your local machine.

```sh
$: python git-mirror.py <GitHub username> <Path to store git repositories>
```

## Installation: ##

Clone this repository:

```sh
$: git clone https://github.com/ermus19/git-mirror
```

[Optional]: Create a virtualenv inside the cloned repository and activate it:

```sh
$: cd git-mirror
$: virtualenv . --python=python3
$: source bin/activate
```

Install the dependencies:

```sh
$: pip install -r requirements.txt
```

## Usage: ##

Run the script:

```sh
$: python git-mirror.py <GitHub username> <Path to store git repositories>
```