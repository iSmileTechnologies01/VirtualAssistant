#!/bin/bash
# Enter the source directory to make sure the script runs where the user expects
apt-get update
apt-get install gcc g++ portaudio19-dev -y 
apt-get install -y cmake build-essential gcc g++ git libsndfile1-dev
apt-get install -y libsm6 libxext6 libxrender1 libfontconfig1
echo "installed"

cd /home/site/wwwroot

if [ -z "$HOST" ]; then
                export HOST=0.0.0.0
fi

if [ -z "$PORT" ]; then
                export PORT=80
fi

export PATH="/opt/python/3.7.9/bin:${PATH}"
echo Found virtual environment .tar.gz archive.
extractionCommand="tar -xzf antenv.tar.gz -C /antenv"
echo Removing existing virtual environment directory '/antenv'...
rm -fr /antenv
mkdir -p /antenv
echo Extracting to directory '/antenv'...
$extractionCommand
PYTHON_VERSION=$(python -c "import sys; print(str(sys.version_info.major) + '.' + str(sys.version_info.minor))")
echo Using packages from virtual environment 'antenv' located at '/antenv'.
export PYTHONPATH=$PYTHONPATH:"/antenv/lib/python$PYTHON_VERSION/site-packages"
echo "Updated PYTHONPATH to '$PYTHONPATH'"
source /antenv/bin/activate
pip install -r /home/update_requirements.txt
GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' --chdir=/home/site/wwwroot" gunicorn app:app
