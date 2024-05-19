Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"  # Use Ubuntu 18.04 LTS
  
    config.vm.network "forwarded_port", guest: 8501, host: 8501  # Forward port for Streamlit
  
    config.vm.provision "shell", inline: <<-SHELL
      # Update package list and install Python and pip
      sudo apt-get update
      sudo apt-get install -y python3-pip
  
      # Create a directory for the app
      mkdir -p /home/vagrant/app
    SHELL
  
    # Copy requirements.txt to the VM
    config.vm.provision "file", source: "requirements.txt", destination: "/home/vagrant/app/requirements.txt"
  
    # Copy app.py to the VM
    config.vm.provision "file", source: "dashboard/app.py", destination: "/home/vagrant/app/app.py"
  
    # Install dependencies from requirements.txt and run Streamlit app
    config.vm.provision "shell", inline: <<-SHELL
      cd /home/vagrant/app
      pip3 install -r requirements.txt
  
      # Run Streamlit app in the background
      nohup streamlit run app.py --server.headless true --server.port 8501 --server.address 0.0.0.0 &
    SHELL
  end