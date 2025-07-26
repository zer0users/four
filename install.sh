echo "Installing four.."
sudo -v
echo "- Getting four latest version.."
wget https://raw.githubusercontent.com/zer0users/four/refs/heads/main/install-files/four
echo "- Giving permissions.."
chmod +x four
echo "Moving into user programs.."
sudo mv four /usr/bin/four
echo "Four installation Done! You can run 'four' on the terminal."
