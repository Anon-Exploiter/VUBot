# For building alpine binary to be used in docker image of
# Gitlab CI -- for CI/CD pipelines

# From https://github.com/six8/pyinstaller-alpine
# docker build -t python3.7:pyinstaller-alpine -f python3.7.Dockerfile .
docker run --rm \
    -v "${PWD}:/src" \
    python3.7:pyinstaller-alpine \
    --noconfirm \
    --onefile \
    --log-level DEBUG \
    --clean \
    vu.py


# Clean local directory
echo "Cleaning up build files -- provide pswd"
sudo rm -rfv __pycache__ build vu.spec