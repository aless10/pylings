#!/usr/bin/env bash
set -euo pipefail

echo "Let's get you set up with pylings!"

echo "Checking requirements..."
if [ -x "$(command -v git)" ]
then
    echo "SUCCESS: Git is installed"
else
    echo "ERROR: Git does not seem to be installed."
    echo "Please download Git using your package manager or over https://git-scm.com/!"
    exit 1
fi

if [ -x "$(command -v python3)" ]
then
    echo "SUCCESS: python is installed"
else
    echo "ERROR: python does not seem to be installed."
    echo "Please download python using https://www.python.org/downloads/!"
    exit 1
fi


echo "Checking python 'installer'..."

Installer="${1-poetry}"

if [[ "$Installer" = "virtualenv" ]]
then
  if [ -x "$(command -v virtualenv)" ]
  then
      echo "SUCCESS: virtualenv is installed"
      InstallCommand="virtualenv venv && source venv/bin/activate && python3 -m pip install ."
      ExecCommand="pylings"
  else
      echo "ERROR: virtualenv does not seem to be installed."
      echo "Please install virtualenv => https://virtualenv.pypa.io/en/latest/installation.html!"
      exit 1
  fi
else
  if [ -x "$(command -v poetry)" ]
  then
      echo "SUCCESS: poetry is installed"
      InstallCommand="poetry install"
      ExecCommand="poetry run pylings"
  else
      echo "ERROR: poetry does not seem to be installed."
      echo "Please download poetry => https://python-poetry.org/docs/#installation!"
      exit 1
  fi

fi

# Function that compares two versions strings v1 and v2 given in arguments (e.g 1.31 and 1.33.0).
# Returns 1 if v1 > v2, 0 if v1 == v2, 2 if v1 < v2.
function vercomp() {
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    v1=( ${1//./ } )
    v2=( ${2//./ } )
    len1=${#v1[@]}
    len2=${#v2[@]}
    max_len=$len1
    if [[ $max_len -lt $len2 ]]
    then
        max_len=$len2
    fi

    #pad right in short arr
    if [[ len1 -gt len2 ]];
    then
        for ((i = len2; i < len1; i++));
        do
            v2[$i]=0
        done
    else
        for ((i = len1; i < len2; i++));
        do
            v1[$i]=0
        done
    fi

    for i in `seq 0 $max_len`
    do
        # Fill empty fields with zeros in v1
        if [ -z "${v1[$i]}" ]
        then
            v1[$i]=0
        fi
        # And in v2
        if [ -z "${v2[$i]}" ]
        then
            v2[$i]=0
        fi
        if [ ${v1[$i]} -gt ${v2[$i]} ]
        then
            return 1
        fi
        if [ ${v1[$i]} -lt ${v2[$i]} ]
        then
            return 2
        fi
    done
    return 0
}

PythonVersion=$(python3 --version | cut -d " " -f 2)
MinPythonVersion=3.7
vercomp "$PythonVersion" $MinPythonVersion || ec=$?
if [ ${ec:-0} -eq 2 ]
then
    echo "ERROR: Python version is too old: $PythonVersion - needs at least $MinPythonVersion"
    exit 1
else
    echo "SUCCESS: Python is up to date"
fi

Path=${1:-pylings/}
echo "Cloning pylings at $Path..."
git clone -q https://github.com/aless10/pylings "$Path"

cd "$Path"

Version=$(curl -s https://api.github.com/repos/aless10/pylings/releases/latest | python3 -c "import json,sys;obj=json.load(sys.stdin);print(obj['tag_name']);")

if [[ -z ${Version} ]]
then
    echo "The latest tag version could not be fetched remotely."
    echo "Using the local git repository..."
    Version=$(ls -tr .git/refs/tags/ | tail -1)
    if [[ -z ${Version}  ]]
    then
        echo "No valid tag version found"
        echo "pylings will be installed using the main branch"
        Version="main"
    else
        Version="tags/${Version}"
    fi
else
    Version="tags/${Version}"
fi

echo "Checking out version $Version..."
git checkout -q ${Version}

echo "Installing the 'pylings' requirements..."
$InstallCommand

echo "All done! Run '${ExecCommand}' to get started."
