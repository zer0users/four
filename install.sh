echo "Installing four.."
sudo -v
wget https://raw.githubusercontent.com/zer0users/four/refs/heads/main/install-files/four
chmod +x four
sudo mv four /usr/bin/four
echo "Four installation Done! You can run 'four' on the terminal."
