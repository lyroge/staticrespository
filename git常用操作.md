### Generating SSH Keys
ssh-keygen -t rsa -C "your email address"

Generate id_rsa & id_rsa.pub files


### Add your SSH key to GitHub

### ssh 常见命令
#链接到git服务器测试
ssh -T git@github.com

#Start SSH agent in the background
eval "$(ssh-agent -s)"
ssh-add -l #view 

The SSH keys on GitHub.com should match the same keys on your computer.

### ssh 常见问题



 

