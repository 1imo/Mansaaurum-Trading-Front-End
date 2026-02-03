#!/bin/bash

# Password for server
PASSWORD=""

# Check if expect is installed (needed for password authentication)
if ! command -v expect &> /dev/null; then
    echo "Error: expect is not installed."
    echo "Install it: brew install expect"
    exit 1
fi

# Build and save the image for linux/amd64 platform
echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t mansaaurum-web:latest .

echo "Saving Docker image..."
docker save mansaaurum-web:latest -o mansaaurum-web.tar

# Copy the image to the server using password authentication
echo "Copying image to server..."
expect << EOF
set timeout 30
spawn scp -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no -o PreferredAuthentications=password mansaaurum-web.tar root@172.245.43.43:/tmp/
expect {
    "password:" {
        send "$PASSWORD\r"
        exp_continue
    }
    eof
}
EOF

# SSH into server and deploy
echo "Deploying on server..."
expect << EOF
set timeout 30
spawn ssh -o StrictHostKeyChecking=accept-new -o PubkeyAuthentication=no -o PreferredAuthentications=password root@172.245.43.43
expect {
    "password:" {
        send "$PASSWORD\r"
        exp_continue
    }
    "# " {
        send "docker load -i /tmp/mansaaurum-web.tar\r"
        expect "# "
        send "docker stop mansaaurum-web 2>/dev/null || true\r"
        expect "# "
        send "docker rm mansaaurum-web 2>/dev/null || true\r"
        expect "# "
        send "docker run -d --name mansaaurum-web -p 4003:4003 --restart unless-stopped mansaaurum-web:latest\r"
        expect "# "
        send "rm -f /tmp/mansaaurum-web.tar\r"
        expect "# "
        send "docker ps | grep mansaaurum-web\r"
        expect "# "
        send "exit\r"
        expect eof
    }
    eof
}
EOF

# Clean up local tar file
rm -f mansaaurum-web.tar

echo "Deployment finished!"
